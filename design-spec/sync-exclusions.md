---
title: OpenAOS Spec Sync — Tenet-Check Exclusions
file_type: design_spec
project: OpenAOS
openaos_version: 3.2.0
created_date: 2026-08-05
last_updated: 2026-08-05
status: design_ready_for_generation
---

# OpenAOS Spec Sync — Tenet-Check Exclusions

Part of the OpenAOS Design Specification document set. The canonical design is in
`openaos-design-spec.md`; the sync procedure is runbook §36.3.

Every plugin → spec sync (§36.3) checks each changed file against the five
fundamental design tenets in runbook §33.1 before reflecting it. A change that
fails is **not** reflected. It is recorded here rather than silently dropped, so
that the decision is visible, dated, and reviewable — a conflicting edit is a
signal to stop and decide, not something a sync absorbs.

This file is tracked because it is a record of design decisions, unlike the local
sync state file (`.openaos-sync-state.json`), which is machine bookkeeping and is
gitignored.

**How an open entry gates a review.** The §34 Design Readiness Checklist reads
this file. An entry whose **Disposition** is still `open` is recorded as a finding
on the §36.1 step 4 issue list — the same list that already gates finalization. So
an undecided tenet conflict does not stop a review from *running*, but it does stop
one from *finalizing*, which is the right shape: an unresolved conflict between a
plugin-side change and a fundamental design tenet is a decision the project owes
itself, and it should not be possible to declare the design ready while one is
outstanding. An entry clears by recording any disposition below — including
`reverted`, which is an explicit decision not to pursue the change. The judgment
stays with the reviewer; only the *record* of it is required.

## How to record an entry

Append a row per excluded file, newest last. Fields:

- **Date** — the date of the §36.3 run that excluded it.
- **File** — plugin-relative path, e.g. `skills/build-workflow/SKILL.md`.
- **Tenet** — the §33.1 tenet number and short name.
- **What was attempted** — one sentence on the plugin-side change.
- **Disposition** — `open` (undecided), `reverted` (the plugin edit was undone),
  `redesigned` (the intent was pursued through a proper spec change instead), or
  `accepted-as-spec-change` (the tenet itself was revisited and changed by a
  `Proceed`-gated spec edit; rare, and should cite the revision-history row).

## Exclusions

| Date | File | Tenet | What was attempted | Disposition |
| ---- | ---- | ----- | ------------------ | ----------- |
| 2026-08-12 | `skills/setup-openaos/SKILL.md` | 1 — Scope discipline | A setup-interview question asking which connectors to use (Google Workspace / Microsoft 365 / Dropbox / connect later), introducing a connector concept the 3.0 Minimal design does not have, and capturing nothing under §7B.2. | `redesigned` — on review the change did not require a tenet amendment. Capturing which tools a user works in is already in scope via `memory-seeds`; the shipped question was a pre-optioned instance of it that failed **§7B.2** (captured nothing) rather than tenet 1. Pursued as a proper spec change instead: §20.1 defines the seed, §12.1(a) defines its one consumer, and the question is recast as `work-platform`. Tenet 1 is unchanged. See the 2026-08-12 revision-history row. |
