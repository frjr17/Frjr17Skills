---
name: plan-phases
description: Turn a proposal, a goal or a review request into a phased plan file in the repo (docs/PLAN_<NAME>.md) with a decisions table, then stop for the user's answers. Use when asked to plan, audit-then-plan, or "divide this into phases".
argument-hint: "<proposal file | goal | what to review>"
disable-model-invocation: true
effort: high
---

# Plan in phases

Input: $ARGUMENTS — a proposal file (PDF/MD), a goal, or an area to review (performance, UX,
security, simplicity…).

## 1. Understand before planning

- Read the repo's `AGENTS.md`, its docs map, the current code that the work touches, and the
  proposal if there is one. Check `git log` and any existing `docs/PLAN*.md` so the plan starts
  from what is really there.
- For a review, judge it as a senior specialist in that area would, and be critical: list
  every real problem with its evidence (file, measurement, screen), not generic advice.

## 2. Write `docs/PLAN_<NAME>.md`

Sections, in this order:

1. **Goal** — two or three sentences; what is out of scope.
2. **Status** — a table: phase, state (todo / in progress / done), commits. `/phase` updates it.
3. **Phases** — IDs with one letter and a number (P1, P2… or the letter the repo already uses).
   Each phase: goal; steps (one step = one commit); acceptance criteria a user can check;
   validation commands; what it changes in stored data (schema/migrations) if anything.
   Order them so every phase leaves the app working and releasable.
4. **Decisions** — table Q1…Qn: question, options, my recommendation and why, answer (empty).
   Only questions whose answer changes the work; defaults I can choose myself go in the plan
   as stated assumptions instead.
5. **Risks and unverified** — what the plan assumes but nobody has checked.

## 3. Commit and stop

- Commit the plan alone: `📝 docs(plan): <name> plan, phases <first>–<last>`.
- Reply with a short summary of the phases and the Q list, recommended option first, numbered
  so I can answer "1. A, 2. as you recommend…". Do not start implementing.
