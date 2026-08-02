---
title: Learning Assistant — Builder Spec
file_type: workflow_spec
slug: learning-assistant
openaos_version: 3.1.0
---
# Learning Assistant — Builder Spec

## Purpose

Guided learning with understanding checks: help the user actually learn a
topic — not just read about it — with explanations at the right level,
comprehension verified before building further, and progress remembered
between sessions.

## Situation Interview

```yaml
- id: learning-goal
  ask: What do you want to learn, and what would being "done" let you do?
  type: text
  default: none
  skippable: no
  when: always
  captures: the goal and the observable outcome in Purpose / Completion Criteria

- id: starting-point
  ask: What do you already know about it? (nothing, the basics, patchy but experienced)
  type: text
  default: none — assessed in the first session
  skippable: yes
  when: always
  captures: the starting level in Inputs

- id: learning-style
  ask: What works for you — examples first, theory first, or learning by doing?
  type: choice
  options: [examples first, theory first, learning by doing]
  default: examples first
  skippable: yes
  when: always
  captures: how Steps orders explanation, practice, and theory

- id: session-shape
  ask: How long is a typical session, and how often?
  type: text
  default: 30 minutes, a few times a week
  skippable: yes
  when: always
  captures: lesson sizing in Steps; cadence in When to Use

- id: materials
  ask: Are you learning from specific materials (a book, a course, docs), or should the workflow choose?
  type: text
  default: workflow proposes materials
  skippable: yes
  when: always
  captures: the source list in Inputs
```

## Baked-In Best Practices

```text
- Check-understanding loops: after each concept, verify comprehension with a
  question or exercise before building on it — and adjust level on a miss
  rather than pushing on.
- Session recap and recall: open each session by recalling the last one;
  close by summarizing what was learned and what comes next.
- Learn by producing: prefer exercises where the user explains, applies, or
  builds, over passive re-reading.
- Track progress durably: keep a progress note (topic map, current position,
  weak spots) as a data file the workflow updates each session.
- Honest difficulty: name what is hard and revisit weak spots; never mark a
  topic learned on the user's behalf.
- Render a session recap as HTML using the shipped
  `learning-assistant-report-template.html` (§18.2, §12.5 condition met: a
  recurring, structured, user-facing report), saved to
  `/outputs/learning-assistant-<date>.html`; the progress note itself stays
  a markdown data file.
```

## Default Skeleton

Per §16.3 section: **Inputs** — goal, starting point, materials, the
progress note. **Steps** — recall, teach one increment (in the chosen
style), check understanding, practice, recap, update progress, render the
session recap as HTML. **Decision Points** — advance vs. revisit on a
failed check; when to propose adjusting the plan. **Approval Gates** — none
beyond §3 (progress notes append; nothing external). **Outputs** — the
updated progress note (stays markdown); any produced exercises in
/outputs; a session recap rendered as HTML using
`/templates/learning-assistant-report-template.html`, saved to
`/outputs/learning-assistant-<date>.html`. **Completion Criteria** — the
user can do the thing the goal named, demonstrated, not assumed.

## Notes

The tempting failure is coverage over comprehension — moving through
material at reading speed. The understanding checks are the workflow's
backbone; refinement may change everything else, but a learning workflow
without checks has lost its point.
