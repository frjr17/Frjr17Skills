---
name: all-phases
description: Carry out every remaining phase of the repo's active plan (docs/PLAN_<NAME>.md), in order and back to back, each to its definition of done, then stop for review. Use when the user says "run all phases", "do the whole plan", "all faces" or "termina el plan".
argument-hint: "[plan name, when the repo has more than one active plan]"
disable-model-invocation: true
model: sonnet
---

# Run all phases

Input: $ARGUMENTS — optional; names the plan when `docs/` holds more than one active plan.

## Before starting

- Open the active plan (`docs/PLAN*.md`, not `docs/history/`). If there are several and no
  argument picks one, ask which. Read the repo's `AGENTS.md` for its commands and rules.
- From the Status table, list the phases still todo or in progress, in plan order (P0…P9, or
  whatever IDs the plan uses). A phase marked in progress resumes at its first uncommitted step.
- Collect every unanswered decision that any of those phases depends on and ask them all now,
  in one numbered list with your recommendation first, so the run doesn't stop halfway for one.
  Record the answers in the plan's decisions table.
- Check the branch. On `main`, `master` or `develop`, stop and ask which branch to use.
- Reply with the phases you will run, then start without waiting.

## Each phase

Same rules as `/phase`:

- One commit per step, gitmoji subject in English, without asking. No AI attribution.
- Stored data changes go through the repo's full checklist (schema version, rules, backup,
  seed, tests), as its `AGENTS.md`/developer docs describe.
- Add or update tests with each step. Never skip, delete or loosen a failing test to get green.
- Keep seed/demo data able to show the new feature.
- While working, run only the tests that cover what you changed.

A phase is done when every step is committed, the working tree is clean, lint, types, unit
tests and build pass, and the plan's Status (phase → done, commits) and the repo's decision and
validation docs are updated, with a last `📝 docs` commit if they changed. Then go straight on
to the next phase; don't stop for review between phases.

## When to stop early

- A decision comes up that the plan didn't foresee and the answer changes the work.
- A check fails and you can't make it pass without loosening a test or leaving the phase's scope.
- A phase's acceptance criteria can't be met as written.

Stop at the end of the last finished phase: committed, clean tree, Status up to date. Say what
blocked, what you tried, and what you need.

## At the end

- Run the full E2E suite once, in the background, if the repo has one; never re-run it to
  "double-check". Report the numbers (tests passed/skipped) for every suite you ran.
- Reply with, per phase: what was done (commits) and how to try it (commands, seed accounts,
  clicks). Then what is left in the plan, if anything, and anything still unverified.
- Never push, deploy or touch CI: I do that.
