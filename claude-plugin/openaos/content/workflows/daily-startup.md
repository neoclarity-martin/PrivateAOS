---
title: Daily Startup Workflow
file_type: workflow
openaos_version: 2.4.2
created_date: 2026-07-17
last_updated: 2026-07-17
status: active
---
# Daily Startup Workflow

## Purpose
Help you start the day by reviewing priorities, commitments, inbox items,
and recently processed inbox items. Review question: **What matters today?**

## When to Use
Daily, at the start of the working day (or on demand: "run my daily
startup").

## Inputs
Yesterday's end-of-day carryover, `/inbox` and `/inbox/processed`,
`/logs/decision-log.md` (recent entries), `/memory/decisions.md`.

## Outputs
A startup brief with these sections, in order: Items processed; Items still
unresolved; Where items were promoted to; Items requiring user approval.

## Steps
1. Read the inputs; do not modify them.
2. Gather today's commitments and open follow-ups.
3. Produce the startup brief (the four sections above).
4. Ask: "What matters today?" and capture the answer as the day's priorities.

## Decision Points
Items needing approval are listed in the brief, never acted on here.

## Approval Gates
None beyond the governance rules — this workflow reads and reports; it
changes nothing.

## Escalation Triggers
Anything in the inbox that looks urgent or sensitive is surfaced to you
first, before any other item.

## Completion Criteria
The brief is delivered and today's priorities are stated.
