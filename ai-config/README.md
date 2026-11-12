# ai-config

My rules for Claude Code and Codex, the commit guard and the cloud-session start hook. This repo
is public: no names, emails or secrets in it.

- `RULES.md` — how I work, in every repo. Linked as `~/.claude/CLAUDE.md` and copied into
  `~/.codex/AGENTS.md` by Frjr17Setup's `aiConfig.sh`; printed into cloud sessions by the hook.
- `git-hooks/commit-msg` — refuses an AI author or committer, drops attribution lines, requires a gitmoji.
- `scripts/session-start.sh` (`hooks/hooks.json`) — in a cloud session: commits as the developer, unsigned,
  installs the commit guard and prints the rules. Everywhere: prints the repo state.
- `claude-settings.json`, `codex-config.toml`, `codex-header.md` — the tools' settings.

## A new repo

Copy `templates/new-repo/` into the repo's root (keep the `.claude/` folder), then fill in
`AGENTS.md`. `.claude/settings.json` turns this plugin on for cloud sessions and empties Claude
Code's own commit and pull request attribution; add the other plugins you want to
`enabledPlugins` (`panama-tech-compliance@frjr17-skills`, `harden-web-security@frjr17-skills`, …).

## A new cloud environment

1. Environment menu → Edit: set the variables `GIT_COMMIT_NAME` and `GIT_COMMIT_EMAIL` (they hold
   personal data: environment only, never a repo). Add a setup script only for dependencies; it
   cannot read the environment's variables or secrets. Pick the network policy.
2. Repos are chosen per session, not per environment. A private repo a setup script needs goes
   under Repositories in the environment's settings.
3. The repo must carry the template above: without `.claude/settings.json` the plugin is off, the
   variables are never read and the session commits as Claude.
4. First session: check it starts with "commits … authored by the repo's developer" and prints the rules.
