"""PreToolUse hook: block Edit/Write that adds an import forbidden by the dependency rule.

Contracts are read from [tool.importlinter] in pyproject.toml, so this hook and
`make lint` can never disagree. Exit 2 blocks the tool call; stderr goes back to Claude.
"""

import json
import os
import re
import sys
import tomllib
from pathlib import Path

# The plugin lives outside the repo, so the project comes from Claude Code, not __file__.
PROJECT_DIR = Path(os.environ["CLAUDE_PROJECT_DIR"])
SRC_DIR = PROJECT_DIR / "src"

IMPORT_RE = re.compile(r"^\s*import\s+(.+)$")
FROM_RE = re.compile(r"^\s*from\s+(\.*[\w.]*)\s+import\b")


def load_contracts() -> list[tuple[str, list[str], str]]:
    config = tomllib.loads((PROJECT_DIR / "pyproject.toml").read_text())
    contracts = config["tool"]["importlinter"]["contracts"]
    return [
        (source, c["forbidden_modules"], c["name"])
        for c in contracts
        if c.get("type") == "forbidden"
        for source in c["source_modules"]
    ]


def module_of(file_path: Path) -> str | None:
    try:
        rel = file_path.resolve().relative_to(SRC_DIR.resolve())
    except ValueError:
        return None
    parts = list(rel.with_suffix("").parts)
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def imported_modules(code: str, current_module: str, is_package: bool) -> list[str]:
    # A code fragment from Edit is often not valid Python, so ast is not an option.
    package = current_module if is_package else current_module.rpartition(".")[0]
    found: list[str] = []
    for line in code.splitlines():
        if m := FROM_RE.match(line):
            target = m.group(1)
            dots = len(target) - len(target.lstrip("."))
            if dots:
                base = package.split(".")
                base = base[: len(base) - (dots - 1)]
                rest = target.lstrip(".")
                target = ".".join(base + ([rest] if rest else []))
            found.append(target)
        elif m := IMPORT_RE.match(line):
            for name in m.group(1).split("#")[0].split(","):
                found.append(name.split(" as ")[0].strip())
    return [f for f in found if f]


def new_code(tool_input: dict) -> str:
    if "content" in tool_input:
        return tool_input["content"]
    if "edits" in tool_input:
        return "\n".join(e.get("new_string", "") for e in tool_input["edits"])
    return tool_input.get("new_string", "")


def matches(module: str, prefix: str) -> bool:
    return module == prefix or module.startswith(prefix + ".")


def main() -> int:
    raw = sys.stdin.read()
    if not raw.strip():
        return 0
    try:
        tool_input = json.loads(raw).get("tool_input") or {}
    except (json.JSONDecodeError, AttributeError):
        return 0

    file_path = tool_input.get("file_path", "")
    if not file_path.endswith(".py"):
        return 0
    path = Path(file_path)
    current = module_of(path)
    if current is None:
        return 0

    imports = imported_modules(new_code(tool_input), current, path.name == "__init__.py")
    violations = [
        f"  {imp}  ←  {name}"
        for source, forbidden, name in load_contracts()
        if matches(current, source)
        for imp in imports
        for f in forbidden
        if matches(imp, f)
    ]
    if not violations:
        return 0

    print(
        f"Dependency rule violation in {current}:\n"
        + "\n".join(violations)
        + "\nSee ARCHITECTURE.md (Dependency rule). Depend on a domain Protocol instead;"
        " wiring of infrastructure happens only in main.py.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
