---
title: Writing Assistant — Builder Spec
file_type: workflow_spec
slug: writing-assistant
openaos_version: 3.0.0
---
# Writing Assistant — Builder Spec

## Purpose

Drafting and editing keyed to the user's voice: produce written work that
sounds like the user on their best day, through a draft-then-critique loop
they control.

## Situation Interview

```yaml
- id: writing-kinds
  ask: What do you write most? (emails, reports, posts, proposals, documentation, personal writing)
  type: text
  default: none
  skippable: no
  when: always
  captures: the document kinds in When to Use and per-kind guidance in Steps

- id: voice-samples
  ask: Can you point to two or three pieces of your writing you're happy with?
  type: text
  default: none — voice is elicited by description instead
  skippable: yes
  when: always
  captures: the voice reference list in Inputs

- id: voice-description
  ask: How would you describe how you want to sound? (formal, direct, warm, playful, technical)
  type: text
  default: none
  skippable: no
  when: always
  captures: the voice notes the critique pass checks against

- id: involvement
  ask: Do you want to shape the outline first, or see a full draft and react?
  type: choice
  options: [outline first, full draft first]
  default: outline first
  skippable: yes
  when: always
  captures: the ordering of Steps

- id: hard-limits
  ask: Anything the workflow must never do in your name? (commit you to something, use certain phrases, exceed a length)
  type: text
  default: none
  skippable: yes
  when: always
  captures: standing constraints in Decision Points
```

## Baked-In Best Practices

```text
- Capture voice explicitly: keep the voice description and sample references
  in the workflow, and check drafts against them by name.
- Draft-then-critique: every draft gets a critique pass against the user's
  stated standard (voice, purpose, audience, limits) before it is shown.
- Preserve the user's meaning: editing sharpens what the user wants to say;
  it never substitutes a different point.
- The user owns the send: drafts stay drafts — publishing or sending in the
  user's name is Level 2 (§3.2).
- Iterate in small deltas: revise the flagged parts, not wholesale rewrites,
  unless asked.
```

## Default Skeleton

Per §16.3 section: **Inputs** — the assignment (what, for whom, why), voice
references, and constraints. **Steps** — clarify the assignment, outline or
draft per the involvement answer, critique against voice and purpose,
revise, deliver. **Decision Points** — the user's hard limits; when a
critique finding warrants asking rather than fixing. **Approval Gates** —
anything leaving the workspace in the user's name. **Outputs** — the piece,
in /outputs or where the user keeps that kind of writing. **Completion
Criteria** — the user says it sounds like them and does the job.

## Notes

Voice drift is the long-run risk: as the user's writing evolves, refinement
should update the samples and description rather than accreting exceptions.
