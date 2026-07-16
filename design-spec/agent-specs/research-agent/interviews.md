---
title: Research Agent — Agent Interviews
file_type: interview_script
slug: research-agent
spec_version: 2.4.1
---
# Research Agent — Interviews

## Initialization Interview

```yaml
- id: research-domains
  ask: What research topics or domains should this agent focus on, and what output format do you prefer (brief, comparison, synthesis)?
  type: text
  default: none
  skippable: no
  when: always
  captures: research-config.md domains; research-output-template.md format

- id: web-search
  ask: Should web search be requested for this agent in the tool access matrix (§22)?
  type: boolean
  default: yes
  skippable: yes
  when: always
  captures: tool-access-matrix.md request row (granted only via Security Agent)

- id: source-reporting
  ask: How should sources and confidence be reported?
  type: text
  default: citations plus a confidence note per finding
  skippable: yes
  when: always
  captures: research-output-template.md citation and confidence conventions
```

## Update Interview

No questions — no migration required at this release.
