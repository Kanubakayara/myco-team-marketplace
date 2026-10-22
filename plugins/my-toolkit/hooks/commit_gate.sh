#!/usr/bin/env bash
# PreToolUse(Bash): block `git commit` unless make lint && make test are green.
# Exit 2 blocks the tool call; stderr goes back to Claude.
set -uo pipefail

command=$(jq -r '.tool_input.command // empty')
[[ "$command" =~ (^|[^[:alnum:]_-])git[[:space:]]+commit([[:space:]]|$) ]] || exit 0

cd "$CLAUDE_PROJECT_DIR" || exit 0
for target in lint test; do
  if ! output=$(make "$target" 2>&1); then
    echo "commit gate: make $target failed — commit blocked" >&2
    tail -n 25 <<<"$output" >&2
    exit 2
  fi
done
