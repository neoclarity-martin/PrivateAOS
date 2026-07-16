---
title: Inbox Agent — Agent Interviews
file_type: interview_script
slug: inbox-agent
spec_version: 2.4.1
---
# Inbox Agent — Interviews

## Initialization Interview

```yaml
- id: inbox-sources
  ask: What sources feed the inbox?
  type: text
  default: none
  skippable: no
  when: always
  captures: inbox-config.md sources

- id: triage-taxonomy
  ask: What triage taxonomy do you use?
  type: text
  default: urgent / waiting / FYI / archive
  skippable: yes
  when: always
  captures: inbox-config.md triage taxonomy

- id: drafting
  ask: Should the agent draft replies automatically, and in what voice?
  type: text
  default: draft for items classified urgent or waiting; neutral professional voice
  skippable: yes
  when: always
  captures: inbox-config.md drafting rules; inbox memory (voice preferences)

- id: promotion-thresholds
  ask: Which promotions should be aggressive vs. conservative?
  type: text
  default: conservative — promote only clear commitments and dated items (§17.5)
  skippable: yes
  when: always
  captures: inbox-config.md promotion thresholds

- id: send-gate
  ask: What sending or publishing must always require Proceed?
  type: text
  default: all sends and publishes (§3.2)
  skippable: yes
  when: always
  captures: inbox-config.md approval boundaries
```

## Update Interview

No questions — no migration required at this release.
