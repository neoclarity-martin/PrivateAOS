---
title: Automation Agent — Agent Interviews
file_type: interview_script
slug: automation-agent
spec_version: 2.4.2
---
# Automation Agent — Interviews

## Initialization Interview

```yaml
- id: automation-targets
  ask: What recurring actions or integrations should be automated?
  type: text
  default: none
  skippable: no
  when: always
  captures: automation memory (automation definitions); automation-config.md scope

- id: tools-involved
  ask: Which tools are involved, and what is their current status in the tool access matrix?
  type: text
  default: none yet — new tools default to Not configured until access is granted (§22)
  skippable: yes
  when: always
  captures: tool-access-matrix.md change requests (granted only via Security Agent)

- id: side-effect-gate
  ask: Confirm that side-effecting runs (send, publish, spend, share, affect others) always require Proceed.
  type: boolean
  default: yes
  skippable: yes
  when: always
  captures: automation-config.md approval boundaries (§3.2)
```

## Update Interview

No questions — no migration required at this release.
