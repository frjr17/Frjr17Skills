@AGENTS.md

## Git (also for cloud sessions, which do not read the owner's personal instructions)

- Commit subjects carry a gitmoji and a type, in English: `✨ feat(scope): …`, `🐛 fix`,
  `♻️ refactor`, `📝 docs`, `🧪 test`, `🎨 style`, `💄 ui`, `⚡️ perf`, `🔒️ security`, `👷 ci`,
  `🔧 chore`, `🔖 release`. The body says what changed and why.
- No AI attribution in commits or pull requests (no `Co-Authored-By`, no "Generated with", no
  session links), and never commit as an AI: check `git config user.name` and `user.email`
  before the first commit. The ai-config plugin sets them and refuses an AI identity.
- A cloud session pushes only its own branch; its pull requests target the default branch's
  integration branch (say which here). Never push to, merge into or deploy from `main`.
- Never tag, deploy, or trigger, re-run or cancel CI workflows.
- Interface text through the app's i18n files; everything else in English. Answer in the
  language the owner writes in.
