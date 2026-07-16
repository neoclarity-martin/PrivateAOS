---
title: Project Manager Agent — Agent Interviews
file_type: interview_script
slug: project-manager-agent
spec_version: 2.4.2
---
# Project Manager Agent — Interviews

## Initialization Interview

```yaml
- id: project-kinds
  ask: What kinds of projects will this agent manage, and at what review cadence?
  type: text
  default: none
  skippable: no
  when: always
  captures: project-manager-config.md scope and cadence

- id: brief-fields
  ask: Which project-brief fields matter most to you (§18.2)?
  type: text
  default: full §18.2 template as-is
  skippable: yes
  when: always
  captures: project-manager memory (brief conventions)

- id: delegation
  ask: How should tasks, research, and stakeholder tracking be delegated?
  type: text
  default: tasks to Task, research to Research, external stakeholders to Personal CRM (when installed)
  skippable: yes
  when: always
  captures: project-manager-config.md collaboration rules (§23)
```

## Update Interview

No questions — no migration required at this release.
