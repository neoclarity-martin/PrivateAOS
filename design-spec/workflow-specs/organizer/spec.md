---
title: Organizer / Declutter — Builder Spec
file_type: workflow_spec
slug: organizer
openaos_version: 3.0.0
---
# Organizer / Declutter — Builder Spec

## Purpose

File cleanup — inbox triage for files: bring an overgrown folder tree back
to a structure the user can navigate, without the workflow ever destroying
anything on its own.

## Situation Interview

```yaml
- id: clutter-locations
  ask: Which folders are the problem? (Downloads, Desktop, Documents, a project folder, the whole workspace)
  type: text
  default: none
  skippable: no
  when: always
  captures: the scope in Inputs — the workflow touches nothing outside it

- id: target-structure
  ask: Do you already have a structure you like, or should the workflow propose one?
  type: choice
  options: [existing structure, propose one]
  default: propose one from what is actually there
  skippable: yes
  when: always
  captures: whether Steps starts from a mapping or a proposal

- id: keep-rules
  ask: What must never be moved or touched? (originals, anything from certain folders, recent files)
  type: text
  default: none
  skippable: no
  when: always
  captures: the exclusion list in Decision Points

- id: duplicate-handling
  ask: When duplicates turn up, what do you want? (list them for me, propose which to archive)
  type: choice
  options: [list them, propose which to archive]
  default: list them
  skippable: yes
  when: always
  captures: the duplicate rule in Steps (archival is always proposed, never automatic)

- id: cadence
  ask: One-time cleanup, or a recurring tidy-up?
  type: choice
  options: [one-time, recurring]
  default: one-time, then recurring monthly if it helped
  skippable: yes
  when: always
  captures: When to Use
```

## Baked-In Best Practices

```text
- Survey before touching: first pass only reads and maps what is there.
- Propose-then-move: every change ships as a written plan — file, from, to,
  why — approved as a batch before anything moves (§3.2 move/bulk-modify).
- Never bulk-delete: the workflow does not delete; candidates for removal
  are proposed for /archive (§30), and even archiving is Level 2.
- Batch by kind: process screenshots, statements, installers, etc. as
  groups, so approval is a readable list rather than a hundred questions.
- Verify after moving: confirm each approved move landed; report anything
  that failed rather than retrying silently.
```

## Default Skeleton

Per §16.3 section: **Inputs** — the scoped folders and the keep rules.
**Steps** — survey and map, propose target structure, plan moves in
batches, execute approved batches, verify, report. **Decision Points** —
the exclusion list; files that fit nowhere go to a proposed "review"
folder, not a guess. **Approval Gates** — every move batch and every
archive proposal (only the §31 /inbox/processed move is pre-authorized).
**Outputs** — the move plan and a completion report. **Completion Criteria**
— scoped folders match the approved structure; nothing deleted; every file
accounted for.

## Notes

Trust is the product here: the first run should be small and visibly
reversible. If the user hesitates at a batch, shrink the batch rather than
argue the plan.
