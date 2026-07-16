---
title: Personal CRM Agent — Agent Interviews
file_type: interview_script
slug: personal-crm-agent
spec_version: 2.4.2
---
# Personal CRM Agent — Interviews

## Initialization Interview

```yaml
- id: relationships-scope
  ask: Which relationships should be tracked, and what context matters?
  type: text
  default: none
  skippable: no
  when: always
  captures: personal-crm memory (relationship context, within /memory/people.md boundaries §20.2)

- id: sensitivity
  ask: What counts as sensitive, requiring approval before storage?
  type: text
  default: standard §20.3 rules; no third-party private information
  skippable: yes
  when: always
  captures: personal-crm-config.md sensitivity rules (coordinated with Security + Memory)

- id: follow-up-cadence
  ask: What follow-up cadence and outreach drafting preferences do you want?
  type: text
  default: surface follow-ups in daily and weekly reviews; draft outreach, never send without Proceed
  skippable: yes
  when: always
  captures: personal-crm-config.md cadence and drafting rules
```

## Update Interview

No questions — no migration required at this release.
