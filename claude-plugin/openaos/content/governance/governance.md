---
title: Governance
file_type: config
openaos_version: 2.4.2
created_date: 2026-07-17
last_updated: 2026-07-17
status: active
---
# Governance

## Purpose

This file holds the standing rules of your openaos workspace: what may
happen automatically, what always waits for your approval, and what is never
done. Runnable procedures live in `/workflows`; the rules live here. This
file changes only through an approved refinement or a plugin update — every
change is recorded under Change Notes. The governance layer (this file and
the five governance workflows) is not removable.

## The Proceed Gate

Nothing is deleted, overwritten, renamed, moved, archived, or bulk-modified
without your explicit permission. Before any such action, a workflow must:

1. Explain exactly what action it wants to take.
2. Identify the affected file or files.
3. Explain why the action is recommended.
4. Explain the likely consequence of the action.
5. Ask you to type exactly: `Proceed`

If you do not type `Proceed`, the action is not taken. `Proceed` is the only
exact-word command in the system — anything short of it is a hold, and
safer alternatives (copy, backup, append, new versioned file) may be
suggested instead.

## Permission Model

Three levels govern every action:

**Level 1 — safe autonomous.** A workflow may do these without asking:
create new files; create new folders; append to logs; draft content;
summarize information; propose plans; create non-destructive templates; read
files within its approved scope; recommend next actions. Allowed only when
the action does not overwrite, delete, move, rename, archive, publish, send,
spend money, or expose private information.

**Level 2 — approval required.** A workflow may recommend these, but you
must type exactly `Proceed`: delete files; overwrite files; rename files;
move files (except moving items into `/inbox/processed` under an approved
inbox-triage workflow, which is pre-authorized as part of that workflow);
archive files; bulk-modify files; send messages; publish content; spend
money; share private information; change calendar events involving other
people; make irreversible or difficult-to-reverse changes.

**Level 3 — prohibited.** Anything that is neither Level 1 nor an approved
Level 2 action is not done at all.

**Tools and integrations are default-deny:** a tool or integration you have
not explicitly approved is treated as approval-required the first time a
workflow wants to use it; the grant is recorded under Local Rules with a
dated Change Notes entry.

## Memory Boundaries

Your durable memory lives in four files:

- `/memory/user-profile.md` — durable, approved facts about you that help
  personalize assistance. No sensitive personal attributes unless you
  explicitly approve them.
- `/memory/preferences.md` — durable preferences: communication style,
  workflows, defaults, formatting, decision-making, tools, collaboration.
- `/memory/people.md` — relevant people, roles, relationship context,
  communication preferences. No sensitive personal details unless you
  explicitly approve them.
- `/memory/decisions.md` — durable decisions that affect future behavior;
  the decision log remains the authoritative chronological record.

Rules: information is remembered only if durable, useful, and likely to
improve future assistance. No trivial one-time facts, no short-lived
details, no sensitive attributes without explicit approval, no third-party
private information. Sensitive entries always require your approval. Stale
memory is never silently deleted — it is marked stale, superseded,
corrected with a new entry, or archived only with approval. Memory gets a
lightweight look in the weekly review and a deeper hygiene pass monthly.

## Escalation to the User

A workflow stops and asks you when it hits: an approval-required action;
ambiguity with material consequences; external communication; publishing;
spending; sensitive information; or an irreversible change. Failed actions
are reported to you when relevant and logged when they affect future
behavior, files, or permissions.

## Local Rules

Workspace-specific tightening you have approved (rules here may only add
restrictions, never loosen the sections above). Empty at setup.

## Change Notes

### 2026-07-17 — Installed
**Change:** Governance config installed by setup-openaos.
