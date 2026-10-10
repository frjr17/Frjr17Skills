# frjr17-skills

Agent Skills marketplace. Ships:

- **harden-web-security** — audit + harden web apps against OWASP-Top-10-and-beyond attacks. Reports each finding with severity, the attacker technique, and a concrete fix.
- **panama-tech-compliance** — audit a system against Panamanian technology law (Ley 81 de 2019 / ANTAI, Ley 51 de 2008, factura electrónica / SFEP, Ley 45 de 2007 / ACODECO, plus fintech, health, public-sector and accessibility regimes). Reports code findings separately from the trámites no code can satisfy. Pre-lawyer triage, not legal advice.
- **workflow** — `/plan-phases` turns a proposal or review into `docs/PLAN_<NAME>.md` with a decisions table; `/phase` carries out a phase or a range to its definition of done (runs on Sonnet).

## Install — Option B: plugin (recommended, versioned, updatable)

```
/plugin marketplace add frjr17/Frjr17Skills
/plugin install harden-web-security@frjr17-skills
/plugin install panama-tech-compliance@frjr17-skills
/plugin install workflow@frjr17-skills
```

Then `/harden-web-security` in Claude Code, or just ask to "harden security" / "run a security review". For the compliance skill: `/panama-tech-compliance`, or ask about "Ley 81", "protección de datos", "factura electrónica", or "cumplimiento legal en Panamá". Update later with `/plugin update`.

## Install — Option A: plain clone (any tool that reads the Agent Skills format)

```bash
git clone https://github.com/frjr17/Frjr17Skills /tmp/Frjr17Skills
cp -r /tmp/Frjr17Skills/harden-web-security/skills/harden-web-security \
      ~/.claude/skills/harden-web-security
```

No versioning or auto-update, but works anywhere `SKILL.md` folders are supported.

## Layout

```
.claude-plugin/marketplace.json           # marketplace manifest
harden-web-security/
├── .claude-plugin/plugin.json            # plugin manifest
└── skills/harden-web-security/SKILL.md   # the skill (single source of truth)
panama-tech-compliance/
├── .claude-plugin/plugin.json
└── skills/panama-tech-compliance/
    ├── SKILL.md                          # router + workflow
    └── references/                       # per-law detail, loaded on demand
        ├── ley-81-datos-personales.md    # tier 1 — start here
        ├── ley-51-firma-electronica.md
        ├── factura-electronica-sfep.md
        ├── ley-45-consumidor.md
        ├── tier-2-sectoriales.md         # fintech, health, public, a11y, licensing
        └── tier-3-tramites.md            # filings; never reported as code findings
workflow/
├── .claude-plugin/plugin.json
└── skills/
    ├── plan-phases/SKILL.md              # /plan-phases
    └── phase/SKILL.md                    # /phase (model: sonnet)
```

Frjr17Setup's `aiConfig.sh` links every `*/skills/*` folder here into `~/.claude/skills` and
`~/.codex/skills`, so the skills keep their short names (`/phase`, not `/workflow:phase`).

## License

MIT (or your choice — add a LICENSE file before publishing).
