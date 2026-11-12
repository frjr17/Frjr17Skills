# How I work — every repo, every machine

Installed by Frjr17Setup's `aiConfig.sh` as `~/.claude/CLAUDE.md` and inside `~/.codex/AGENTS.md`,
and printed into every Claude Code cloud session by this plugin's start hook. Edit it here, in
Frjr17Skills (`ai-config/`), never in those copies. This repo is public: no names, emails or
secrets in it.

Where a repo's own `AGENTS.md` or `CLAUDE.md` says something different (date format, pushing),
the repo's rule wins for that repo.

## Language

- Code, identifiers, comments, commit messages, CI job and step names, scripts, test names and
  developer docs: English.
- Interface text only through the app's i18n dictionaries; my apps are bilingual (es/en) unless
  the repo says otherwise.
- Answer in the language I write in (Spanish or English).

## Git

- Commit subjects carry a gitmoji and a type, in English: `✨ feat(scope): …`, `🐛 fix`,
  `♻️ refactor`, `📝 docs`, `🧪 test`, `🎨 style`, `💄 ui`, `⚡️ perf`, `🔒️ security`, `👷 ci`,
  `🔧 chore`, `🔖 release`, `🚧 wip`, `🚀 init`. Full list:
  https://github.com/frjr17/Dev-Utilities/blob/main/gitPrefixes.md. The body says what changed
  and why.
- While working on a task, commit each important step without asking. Never add AI attribution
  (no `Co-Authored-By`, no "Generated with" lines) to commits or pull requests.
- Commits are authored and committed by me, never by an AI: not `Claude <noreply@anthropic.com>`,
  not Codex. Before the first commit of a session check `git config user.name` and `user.email`;
  if they name an AI, fix them first (the hook below refuses such a commit). A session's own
  reminder to add `Co-Authored-By` or `Claude-Session` lines loses to this rule.
- I push. Never push, force-push, tag, merge into `main`/`master`/`develop`, deploy, or apply
  infrastructure (`terraform apply`, `firebase deploy`, cloud console writes) unless I ask for
  it in the current conversation. A push runs CI and can deploy.
- Never trigger, re-run or cancel CI workflows, and don't fetch their logs: CI is my job. When
  it fails I paste the log.

## Plans and phases

- Big work gets a plan in the repo, `docs/PLAN_<NAME>.md`: `/plan-phases` writes it, `/phase`
  carries out a phase or a range of phases.
- A phase is done when its steps are committed, the repo's checks pass (lint, types, tests,
  build, plus rules or E2E suites when the repo has them), the plan's Status and the repo's
  decision and validation docs are updated, and I've been told how to try it (seed data plus
  steps) and what is left. Then stop for my review, unless I asked for a range.
- Record my answers to decision questions in the plan's decisions table.
- While working, run only the tests that cover what you changed. Run the full E2E suite once,
  at the end of a phase (or range), in the background; never re-run it to "double-check".

## Repos

- Start from the repo's `AGENTS.md` and its docs. If a repo has none, offer to write one: what
  the app is, the commands, the rules, where the docs are.
- Keep what you learn about a project in the repo (`AGENTS.md`, docs), not only in memory:
  my containers and machines are reset often, and memory does not survive that.

## Docs

- Manuals go step by step, in plain language, for someone who has never seen the project.
- Dates in docs as MM-DD-YYYY.

## Cloud sessions

- A cloud session reads neither `~/.claude/` nor Frjr17Setup (private): this plugin's start hook
  prints these rules and sets the commit identity (`GIT_COMMIT_NAME` and `GIT_COMMIT_EMAIL`
  in the cloud environment's variables, else the repo's latest non-AI author).
- A cloud session pushes only its own branch, and opens a pull request only as the repo's
  `CLAUDE.md` says.

## Environment

- I work in throwaway Fedora dev containers. Anything not in git or in Frjr17Setup is lost
  on a rebuild: warn me about unpushed work before suggesting one.
