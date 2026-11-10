# Run-all mode

Runs every recommended, enabled skill in order, from one command. "At once" means
**one request, executed in sequence**. claude.ai has no parallel workers, and later
skills usually need earlier outputs anyway. In Claude Code, independent steps (same
step number, e.g. `3a`/`3b`) may run in parallel subagents.

## 1. Build the run plan

Start from the step-7 table (run the recommendation first if this conversation
doesn't have one). Then:

- **Keep:** enabled picks with a step number.
- **Skip, and say why:** `on-disk-not-enabled` and catalog picks (can't run until
  enabled), near misses, and the losing half of any duplicate pair.
- **Dependencies:** note what each step hands the next (a plan file, a branch, a report).
- **Side effects:** mark steps whose skill sends, publishes, deploys, launches, writes to
  a CRM/ESP/ad account, deletes, or spends money.

## 2. Confirm once

Show the plan as a compact numbered list (step, skill, what it will produce, side
effects) and get **one** confirmation before starting. Running slash-only skills
(`user_invoked_only: true`) is acceptable because the user is invoking them through
this plan, but they must appear by name in the plan they confirm. If the user
already said "run them all, don't ask" and **no** step has side effects, start
directly.

## 3. Execute

For each step, in order:

1. `view` the skill's SKILL.md (and any files it says to read). Follow it fully, exactly
   as if the user had invoked it alone. Don't skim or blend instructions across skills.
2. Feed it the user's task plus the outputs of earlier steps.
3. Append a line to `/tmp/skill-audit-run.md`: step, skill, status
   (done / stopped / failed / skipped), output path or one-line result.

Rules that override "run everything":

- **The skill's own gates win.** If a skill says to stop for the user's answers, ask
  for approval, or wait for review (e.g. `plan-phases` stops for decisions;
  `execute-action` needs an approval record), stop the chain there. Report steps done,
  what's needed, and the remaining steps. `/skill-audit run-all continue` resumes from
  the log.
- **Side-effecting actions are never auto-approved**, even inside a confirmed plan.
  The plan confirmation covers running the skill, not the irreversible action within it.
- **On failure:** record the error, skip only the steps that depend on it, continue
  with independent ones.
- **Continue:** on `run-all continue`, read `/tmp/skill-audit-run.md` (or this
  conversation's last progress report if the file is gone) and resume at the first step
  not done.

## 4. Final report

```
| # | Skill | Result | Output |
|---|---|---|---|
| 1 | workflow:plan-phases | stopped: needs your answers on 3 decisions | docs/PLAN_GHA.md |
| 2 | workflow:all-phases | pending (after step 1) | - |
```

Then: what's needed from the user to continue, skipped skills and how to enable them,
and present any produced files.
