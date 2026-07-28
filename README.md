# frjr17-skills

Agent Skills marketplace. Currently ships one skill:

- **harden-web-security** — audit + harden web apps against OWASP-Top-10-and-beyond attacks. Reports each finding with severity, the attacker technique, and a concrete fix.

## Install — Option B: plugin (recommended, versioned, updatable)

```
/plugin marketplace add frjr17/frjr17-skills
/plugin install harden-web-security@frjr17-skills
```

Then `/harden-web-security` in Claude Code, or just ask to "harden security" / "run a security review". Update later with `/plugin update`.

> Replace `frjr17/frjr17-skills` with your actual `owner/repo` after pushing to GitHub.

## Install — Option A: plain clone (any tool that reads the Agent Skills format)

```bash
git clone https://github.com/frjr17/frjr17-skills /tmp/frjr17-skills
cp -r /tmp/frjr17-skills/harden-web-security/skills/harden-web-security \
      ~/.claude/skills/harden-web-security
```

No versioning or auto-update, but works anywhere `SKILL.md` folders are supported.

## Layout

```
.claude-plugin/marketplace.json          # marketplace manifest
harden-web-security/
├── .claude-plugin/plugin.json           # plugin manifest
└── skills/harden-web-security/SKILL.md  # the skill (single source of truth)
```

## License

MIT (or your choice — add a LICENSE file before publishing).
