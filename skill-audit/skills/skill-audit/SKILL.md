---
name: skill-audit
description: Audit which skills are enabled, installed but switched off, or only available to add; recommend up to 10 that fit a task, in run order; flag duplicate skills; lint skills for defects (health mode); and run every recommended skill in sequence (run-all mode). Use whenever the user asks what skills or plugins they have, whether a skill is installed or enabled, which skill to use or run, what fits a task, to compare, check or lint skills, why a skill didn't trigger, or to run all the recommended skills, in English or Spanish ("qué skills tengo", "cuál skill uso", "córrelas todas"), even if they don't say "audit".
---

# Skill Audit

Answer accurately: **what can be used right now**, **what fits the task and in what
order**, and optionally **run it all**. Accuracy beats coverage: a wrong "you have X"
sends the user chasing a skill that won't run.

## Modes

| Invocation | Mode | Do |
|---|---|---|
| no task, or "what skills do I have" | Inventory | Steps 2-3, then report counts (step 7) |
| a task ("which skills for X") | Recommend | Steps 1-7 |
| `health`, "lint/check my skills" | Health | Steps 2-3 with `--health --overlaps`, report per step 7 |
| `run-all [task]`, "run them all" | Run-all | Recommend first (unless done this conversation), then read `references/run-all.md` |
| one skill by name ("is X installed?") | Single check | Look it up directly: enabled list, then disk, then `search_skills` |

## 1. Extract keywords (both languages)

Take 4-8 keywords from the task, plus synonyms (CI → pipeline, build, deploy). Many
skills trigger on Spanish phrases, so whatever language the user wrote in, include the
key terms in **both English and Spanish** (plan → plan, planificar; phase → fase;
review → revisar). The scorer ignores accents, so "migración" matches "migracion".
Don't ask a clarifying question when the task is inferable from context.

## 2. Build the enabled list (cheaply)

The skill list in your context (`<available_skills>` in claude.ai/Cowork) is the source
of truth for what can run. Don't retype every name. Write `/tmp/enabled.txt` using
shorthand where it is safe:

```
@public                 # every skill under /mnt/skills/public
@plugins                # every installed plugin skill
docs                    # individual names for partially enabled sources
morning
```

Also accepted: globs (`digital-marketing-pro:*`) and raw pasted text containing
`<name>…</name>` tags. **Use `@source` or a glob only when every skill it covers appears
in the context list.** Example skills are usually only partly enabled, so list those by
name. After the run, compare the script's `enabled` count with the length of the
context list. If they differ, your shorthand over- or under-covered; fix the file and rerun.

In Claude Code there's no context list: skip `--enabled-file`. Everything found in the
Claude Code paths counts as installed. Per-surface paths are in `references/environments.md`.

## 3. Run the inventory

```bash
python3 <skill-dir>/scripts/inventory.py --enabled-file /tmp/enabled.txt \
  --query <keywords> --overlaps --format json > /tmp/inventory.json
```

Act on the output:

- `typo_warnings`: an entry matched nothing but resembles a real skill. Fix it and rerun.
  A typo there silently turns an enabled skill into "not enabled".
- `status`: `enabled` (ready), `on-disk-not-enabled` (switched off), `enabled-not-on-disk`
  (listed, but files not inspectable; still usable), `on-disk` (Claude Code).
- `score`: word-match count for shortlisting only. It will rank a marketing skill above
  a CI skill because both say "pipeline". Read the description of **every** skill with
  score > 0 plus any whose name obviously fits, and judge relevance yourself.
- `overlaps`: pairs that duplicate each other. Never recommend both halves of a pair.
- `health` (health mode): severity `error` (broken: can't trigger or missing a file it
  needs), `warn` (works but should be fixed), `info` (environment note, e.g. plugin
  scripts not shipped on this surface, so the skill may run degraded here).

## 4. Check the catalog

If enabled skills don't cover the whole task and `search_skills` exists, call it with
the same keywords (`search_plugins` if the need is a tool bundle). Results flagged
not-enabled are catalog candidates. Never present a skill unless it came from disk, the
enabled list, or a search result. When the search finds nothing for part of the task,
name the gap ("no skill covers GitHub Actions"). That part will run on Claude's general
knowledge.

## 5. Choose (up to 10)

Recommend every skill that genuinely applies, up to **10**. Each must have a concrete
reason tied to the task. A shared word ("plan", "pipeline") doesn't qualify. Missing a
relevant skill and padding with an irrelevant one are equally wrong.

- **Tiers:** Primary (does the core of the task), Supporting (a step, check, or output
  the task needs: security, docs, compliance, a deck), Enable or add (fits, but off or
  catalog-only).
- **Duplicates:** for each overlap pair, pick one. Prefer the more specific description;
  if they're variants (`review` vs `ui-review`), prefer the fuller one and mention the
  other in near misses.
- **More than 10 qualify:** keep the 10 strongest (Primary, then Supporting, then Enable
  or add) and name the rest on an **Also applies:** line.
- **Near misses:** one line of related-sounding skills you excluded, with a few words
  on why.

## 6. Order and how to run

Give each enabled pick a step number reflecting the order to use them:
plan/design → build/execute → review/security/compliance → package/present. A skill
whose output feeds another goes first. Independent skills share a number (e.g. `3a`, `3b`).

For **every** pick, check `user_invoked_only` before writing how to run it. Don't
assume from the name:

- auto-triggering → "ask for X" (it loads itself)
- `user_invoked_only: true` → slash command with its `argument_hint`, e.g. `/phase next`
- `on-disk-not-enabled` → enable in settings first
- catalog → call `suggest_skills` / `suggest_plugin_install` with the same keywords for
  an Add button. One card per conversation; don't repeat an ignored one.

## 7. Report

```
**Inventory:** 193 enabled · 30 on disk but off · 0 user skills
**For <task>:**
| # | Tier | Skill | Status | Why | Run it |
|---|---|---|---|---|---|
| 1 | Primary | workflow:plan-phases | enabled | turns the migration into a phased plan | `/plan-phases <goal>` |
| 2 | Primary | workflow:all-phases | enabled | executes the plan end to end | `/all-phases` |
| 3 | Supporting | harden-web-security | enabled | reviews pipeline secrets and permissions | ask for a CI/CD security review |
| – | Enable or add | ... | on-disk-not-enabled | ... | enable in settings |

**Also applies:** (only if >10) · **Near misses:** campaign-plan, media-plan (marketing, not engineering)
```

Close with a short paragraph: duplicates resolved, gaps, defects that affect the picks,
and anything you couldn't verify. Mention that `run-all` can run the list.

**Inventory mode:** counts by source and status; list names only for groups the user
asked about. **Health mode:** errors first, then warnings, each with the fix. Collapse
`info` lines into one sentence unless asked. Offer the full list as a file only if asked.

## Edge cases

- **Same name in two places:** list both paths and say which one a request would hit.
- **Script fails / no roots:** use the context list alone and say disk status wasn't checked.
- **Skill created in this conversation:** not installed until the user saves the `.skill` file.
