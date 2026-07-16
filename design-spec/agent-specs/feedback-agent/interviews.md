---
title: Feedback Agent — Agent Interviews
file_type: interview_script
slug: feedback-agent
spec_version: 2.4.1
---
# Feedback Agent — Interviews

## Initialization Interview

```yaml
- id: email-capability
  ask: Is an email capability configured for this AOS that can send to aos-factory@neoclarity.ai?
  type: boolean
  default: no — submissions stay staged in the feedback log and you are prompted to send manually
  skippable: yes
  when: always
  captures: feedback-config.md transport note; tool-access-matrix.md Email send row (Approval-required)
```

## Update Interview

No questions — no migration required at this release.
