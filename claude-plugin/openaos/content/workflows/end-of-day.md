---
title: End-of-Day Workflow
file_type: workflow
openaos_version: 2.4.2
created_date: 2026-07-17
last_updated: 2026-07-17
status: active
---
# End-of-Day Workflow

## Purpose
Capture what changed today, what must not be lost, unresolved obligations,
decisions made, follow-ups needed, and next-day carryover. Review question:
**What changed today, and what must not be lost?**

## When to Use
Daily, at the end of the working day (or on demand).

## Inputs
Today's session activity, `/outputs` (today's files), the day's priorities
from the daily startup.

## Outputs
Appended entries: decisions to `/logs/decision-log.md` (decision-entry
template), memory-worthy items proposed for `/memory` (each approved
individually), and a carryover note for tomorrow's startup.

## Steps
1. Ask: "What changed today, and what must not be lost?"
2. Walk through: decisions made, obligations still open, follow-ups needed.
3. Record decisions; propose memory entries (approval per entry, per the
   governance memory rules).
4. Write the next-day carryover note.

## Decision Points
Whether an item is a decision (log it), a memory (propose it), or a task
for tomorrow (carry it over).

## Approval Gates
Every memory entry proposal; anything sensitive.

## Escalation Triggers
An unresolved obligation with a deadline before the next startup is flagged
now, not carried silently.

## Completion Criteria
Decisions logged, proposed memories resolved (approved or dropped),
carryover written.
