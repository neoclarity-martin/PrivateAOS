---
title: Security Agent — Agent Interviews
file_type: interview_script
slug: security-agent
spec_version: 2.4.2
---
# Security Agent — Interviews

## Initialization Interview

```yaml
- id: privacy-sensitivity
  ask: How privacy-sensitive is this AOS? (This scales escalation thresholds.)
  type: choice
  options: [standard, high, very high]
  default: standard
  skippable: yes
  when: always
  captures: security-config.md escalation thresholds

- id: known-tools
  ask: Which tools or integrations are already in use, and at what access level?
  type: text
  default: none known — seed the matrix empty; every tool defaults to Not configured (§22)
  skippable: yes
  when: always
  captures: /configs/tool-access-matrix.md seed rows

- id: extra-approvals
  ask: Any actions that must always require approval beyond the Section 3 defaults?
  type: text
  default: none — adopt the §3 three-level model unchanged
  skippable: yes
  when: always
  captures: /configs/global-permissions.md and security-config.md
```

## Update Interview

No questions — no migration required at this release.
