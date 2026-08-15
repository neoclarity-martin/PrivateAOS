---
title: Inbox Triage — Builder Spec
file_type: workflow_spec
slug: inbox-triage
openaos_version: 3.2.1
---
# Inbox Triage — Builder Spec

## Purpose

Classify, route, and act on inbox items so nothing important sits unread or
gets lost. The generated workflow processes whatever the user treats as an
inbox — email, a notes capture folder, `/inbox`, a messaging backlog — and
promotes each item to where it belongs.

## Situation Interview

```yaml
- id: inbox-sources
  ask: What piles up for you? (email, a notes folder, chat messages, the /inbox folder, something else)
  type: text
  default: the workspace /inbox folder
  skippable: no
  when: always
  captures: the input sources the Steps section reads

- id: item-kinds
  ask: What kinds of things land there? (requests, information, commitments, ideas, junk)
  type: text
  default: none — elicit at first run
  skippable: yes
  when: always
  captures: the classification categories in Decision Points

- id: routing-targets
  ask: When something needs action, where should it go? (a to-do list, your calendar, a person, a folder)
  type: text
  default: none
  skippable: no
  when: always
  captures: the promotion targets in Steps and Outputs

- id: reply-drafting
  ask: Should the workflow draft replies for you to review?
  type: choice
  options: [yes, no]
  default: yes
  skippable: yes
  when: sources include messages
  captures: whether Steps includes a reply-drafting pass (sending is always Level 2)

- id: volume-cadence
  ask: Roughly how many items a day, and when do you want to process them?
  type: text
  default: once daily, with the daily-startup workflow
  skippable: yes
  when: always
  captures: batch size in Steps; cadence in the router row (§16.11)
```

## Baked-In Best Practices

```text
- Classify before acting: decide what each item is before doing anything.
- Batch similar items: group by category and process each group in one pass.
- Route, don't hoard: every item ends promoted, archived, or consciously
  deferred — never silently left behind.
- Draft, never send: replies are drafts; sending is Level 2 (§3.2).
- Moving processed items into /inbox/processed is pre-authorized (§31);
  every other move or deletion follows the §3 rules.
- Surface a triage summary using the §17.1 startup-brief categories, so the
  daily-startup workflow can report on it.
- Render the triage summary as HTML using the shipped
  `inbox-triage-report-template.html` (§18.2, §12.5 condition met: a
  recurring, structured, user-facing report), saved to
  `/outputs/inbox-triage-<date>-<run>.html`.
```

## Default Skeleton

Per §16.3 section: **Inputs** — the elicited sources. **Outputs** — the triage summary
(the four §17.1 brief categories, plus a category breakdown), rendered as
HTML using `/templates/inbox-triage-report-template.html`, saved to
`/outputs/inbox-triage-<date>-<run>.html`. **Steps** — collect, classify
(one pass), then act per category batch: promote, draft, archive, or defer;
render the summary as HTML as the final step. **Decision Points** — the
classification categories with one-line rules for each. **Approval Gates**
— sending, deleting, and any move outside `/inbox/processed`. **Escalation
Triggers** — items the workflow cannot classify, and anything sensitive.
**Completion Criteria** — inbox empty or every remaining item consciously
deferred, with the summary produced.

## Notes

The commonest failure is a workflow tuned to an idealized inbox rather than
the real one — keep the categories to what the user actually receives, and
let refinement add more later. Do not promise to "handle" email: the
workflow triages and drafts; the user sends.
