---
name: phase
description: Carry out one phase, or a range of phases, of the repo's active plan (docs/PLAN_<NAME>.md) to its definition of done, then stop for review. Use when the user says "start P3", "sigue con la F4", "next phase" or names a range.
argument-hint: "<phase id | range like F3..F5 | next>"
disable-model-invocation: true
model: sonnet
---

# Run a phase

Input: $ARGUMENTS — a phase ID (`P3`), a range (`F3..F5`, run them back to back) or `next`.

## Before starting

- Open the active plan (`docs/PLAN*.md`, not `docs/history/`), its Status, and the phase's
  steps and acceptance criteria. Read the repo's `AGENTS.md` for its commands and rules.
- If the plan has unanswered decisions this phase depends on, ask them first, with your
  recommendation.
- Check the branch. On `main`, `master` or `develop`, stop and ask which branch to use.

## Doing the work

- One commit per step, gitmoji subject in English, without asking. No AI attribution.
- Stored data changes go through the repo's full checklist (schema version, rules, backup,
  seed, tests), as its `AGENTS.md`/developer docs describe.
- Add or update tests with each step. Never skip, delete or loosen a failing test to get green.
- Keep seed/demo data able to show the new feature.

## Definition of done

1. Every step committed; the working tree is clean.
2. The repo's checks pass: lint, types, unit tests, build, plus rules or E2E suites if the repo
   has them. Report the numbers (tests passed/skipped).
3. Docs updated: the plan's Status (phase → done, commits), decisions with their reasons, what
   was verified and what wasn't (the repo's DECISIONS/VALIDATION docs or equivalents).
4. A last `📝 docs` commit if step 3 changed anything.

## Reply and stop

- What was done (commits), how to try it (commands, seed accounts, clicks), what's left in the
  plan, and any decision needed for the next phase.
- With a range, go straight on to the next phase and stop at the end of the range, or earlier
  on a blocking decision or a check you can't make pass.
- Never push, deploy or touch CI: I do that.
