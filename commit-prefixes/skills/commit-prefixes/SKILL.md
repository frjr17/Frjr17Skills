---
name: commit-prefixes
description: Create and validate Git commit messages using the repository's approved gitmoji type prefixes. Use whenever a commit message is requested, proposed, reviewed, or created.
---

# Enforce commit prefixes

Apply these rules to every commit message:

- Write the subject in English.
- Start the subject with exactly one approved prefix, followed by an optional scope and a concise subject:
  `gitmoji type(scope?): subject`
- Use one of these approved prefixes:
  - `✨ feat`
  - `🐛 fix`
  - `♻️ refactor`
  - `📝 docs`
  - `🧪 test`
  - `🚀 init`
  - `🎨 style`
  - `👷 ci`
  - `🚧 wip`
  - `🔧 chore`
  - `🔀 merge`
- Keep the subject concise and do not end it with a period.
- When the change is substantial, include a body explaining what changed and why.
- Never add AI attribution, `Co-Authored-By`, or generated-content lines.

Choose the type that matches the primary purpose of the change. Use `merge` only for merge commits and `wip` only when the commit is intentionally incomplete.

Before returning or running a commit command, validate that the message follows the format. If it does not, correct it instead of presenting or using the invalid message.

Examples:

```text
✨ feat(auth): add password reset flow
🐛 fix: handle empty configuration safely
📝 docs: document local development setup
```
