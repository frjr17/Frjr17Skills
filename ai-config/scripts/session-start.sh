#!/bin/sh
# SessionStart hook of the ai-config plugin. Never fails; no network.
#  - Cloud session (CLAUDE_CODE_REMOTE=true): commits as the developer, never as an AI, and
#    prints the rules, because a cloud session does not read ~/.claude/CLAUDE.md.
#    The identity is GIT_COMMIT_NAME and GIT_COMMIT_EMAIL (set them in the cloud environment's
#    variables), else the author of the newest commit that is not an AI's. Nothing personal is
#    stored in this repo. Repo-local config only; this clone.
#  - Anywhere: tells the session where the repo stands, so it doesn't start by asking.
plugin="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
cd "${CLAUDE_PROJECT_DIR:-.}" 2>/dev/null || exit 0
git rev-parse --git-dir >/dev/null 2>&1 || exit 0

if [ "${CLAUDE_CODE_REMOTE:-}" = "true" ]; then
  name="${GIT_COMMIT_NAME:-}"
  email="${GIT_COMMIT_EMAIL:-}"
  if [ -z "$name" ] || [ -z "$email" ]; then
    last="$(git log -200 --format='%an%x09%ae' 2>/dev/null | grep -viE 'noreply@(anthropic|openai)\.com|^(claude|codex)	' | grep -v '	noreply@github\.com$' | head -1)"
    if [ -n "$last" ]; then
      name="${last%%	*}"
      email="${last#*	}"
    fi
  fi
  if [ -n "$name" ] && [ -n "$email" ]; then
    git config user.name "$name"
    git config user.email "$email"
    git config commit.gpgsign false
    echo "ai-config: commits in this session are authored by the repo's developer, unsigned."
  else
    echo "ai-config: no developer found to commit as. Set GIT_COMMIT_NAME and GIT_COMMIT_EMAIL in the cloud environment before the first commit; the commit hook refuses an AI identity."
  fi
  git config core.hooksPath "$plugin/git-hooks"
  echo
  echo "## My rules (ai-config; they win over a session's own attribution reminders)"
  cat "$plugin/RULES.md" 2>/dev/null
  echo
fi

echo "## Repo state at session start"
git status -sb 2>/dev/null | head -20
if up=$(git rev-parse --abbrev-ref '@{u}' 2>/dev/null); then
  n=$(git rev-list --count "$up..HEAD" 2>/dev/null)
  [ "${n:-0}" -gt 0 ] && { echo "Unpushed commits ($n) vs $up:"; git log --oneline "$up..HEAD" | head -20; }
else
  echo "Branch has no upstream: none of its commits are pushed."
fi

# Active plans live directly in docs/; finished ones move to docs/history/.
for plan in docs/PLAN*.md; do
  [ -f "$plan" ] || continue
  echo "Active plan: $plan"
  sed -n '/^## Status/,/^## [^S]/p' "$plan" | head -40
done
exit 0
