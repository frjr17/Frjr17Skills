# Where skills live, per surface

Read only the section for the surface you're running in.

## claude.ai and Cowork (container at /mnt/skills)

| Path | What it is |
|---|---|
| `/mnt/skills/public/` | Anthropic's built-in document skills (docx, pdf, pptx, xlsx...) |
| `/mnt/skills/examples/` | Anthropic example skills. Many ship on disk but are toggled off |
| `/mnt/skills/plugins/<plugin>:<skill>/` | Skills from installed plugins, namespaced by plugin |
| `/mnt/skills/user/` | Skills the user uploaded (may not exist) |
| `/mnt/skills/private/` | Org-provisioned skills (may not exist) |

- **Enabled = listed in `<available_skills>` in your context.** Disk presence alone
  means nothing: it's common to find 200+ SKILL.md files with only a fraction enabled.
- The catalog of skills the user *could* add is reachable only through the
  `search_skills` tool (returns an enabled flag) and `suggest_skills` (renders an Add card).
  Plugins: `search_plugins` / `suggest_plugin_install`. One suggestion card per
  conversation; don't repeat it if ignored.
- The user toggles skills in Settings → Capabilities (claude.ai). Don't guess deeper
  menu paths.
- `/mnt/skills` is read-only. A new skill gets installed by packaging it as a `.skill`
  file and presenting it (the file card has a Save skill button), not by writing there.

## Claude Code

| Path | Scope |
|---|---|
| `~/.claude/skills/<name>/SKILL.md` | Personal, all projects |
| `.claude/skills/<name>/SKILL.md` | Project, committed with the repo |
| `~/.claude/plugins/...` | Installed plugins (skills under each plugin's `skills/` folder) |

- Enabled = present in those locations and from an enabled plugin. `/plugin` shows
  installed and enabled plugins; marketplaces list what's installable.
- Project skills override nothing silently: if the same name exists at two scopes,
  report both paths.
- To install: copy the folder into one of the paths above, or `/plugin install`.

## Frontmatter fields that change the recommendation

- `disable-model-invocation: true` → Claude never auto-triggers it. Recommend it as a
  slash command the user types (`/phase F3`), and show `argument-hint` if present.
- `argument-hint` → the arguments the slash command expects.
- No `name` field → command-style skill; its name is the folder name. Valid.
- No `description` → it can't auto-trigger. Report it as a defect.
- `allowed-tools`, `model` → informational; mention only if relevant to the task.
