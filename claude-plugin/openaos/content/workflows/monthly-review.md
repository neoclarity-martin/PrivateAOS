---
title: Monthly Review Workflow
file_type: workflow
openaos_version: 3.0.0
created_date: 2026-07-17
last_updated: 2026-07-17
status: active
---
# Monthly Review Workflow

## Purpose
Keep the workspace structurally healthy and aimed at the right goals:
memory hygiene, workflow quality, permission boundaries, structural
clutter, and cleanup needs. Review questions: **What is stale, misplaced,
or structurally messy?** and **Is the whole system still aimed at the right
goals?**

## When to Use
Monthly (or on demand).

## Inputs
All `/memory` files (deep pass), the month's weekly-review flags,
`/governance/governance.md` (Local Rules + Change Notes), `/logs`,
`/workflows` (the installed list), `/docs/user-guide.html`.

## Outputs
A health report; proposed memory cleanups (each approved individually); a
regenerated User Guide; feedback candidates; workflow suggestions.

## Steps
1. Deep memory hygiene pass: for each flagged or aging entry, propose mark
   stale / supersede / correct / archive — every change approved
   individually, nothing silently deleted.
2. Review permission boundaries: walk through governance.md Local Rules and
   tool grants; propose revoking any that are no longer used.
3. Structural pass: stale files, misplaced items, clutter; propose cleanups
   (archiving is approval-required).
4. Goal alignment: ask whether the installed workflows still support your
   priorities. Suggest building a workflow for an observed gap, or refining
   or archiving one that no longer earns its place. **Anti-nagging rule:**
   a declined suggestion is logged and not re-raised until the next monthly
   review or a material change in usage.
5. Feedback self-examination: review recent friction and errors for
   enhancement candidates; present each for accept / edit / discard;
   accepted items enter the feedback workflow.
6. Regenerate `/docs/user-guide.html` from what is actually installed,
   preserving its embedded change log.

## Decision Points
Per memory entry: stale / supersede / correct / archive / leave. Per
suggestion: accept / decline (log it).

## Approval Gates
Every memory change, every archive, every cleanup, the user-guide
regeneration (an overwrite), and anything leaving the machine (via the
feedback workflow only).

## Escalation Triggers
Any sign that a governance rule was bypassed or weakened is raised
immediately and logged.

## Completion Criteria
Health report delivered; approved changes applied and logged; user guide
regenerated; declined suggestions logged.
