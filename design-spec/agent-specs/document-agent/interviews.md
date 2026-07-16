---
title: Document Agent — Agent Interviews
file_type: interview_script
slug: document-agent
spec_version: 2.4.1
---
# Document Agent — Interviews

## Initialization Interview

```yaml
- id: document-scope
  ask: What document types and sources need cataloging?
  type: text
  default: none
  skippable: no
  when: always
  captures: document-config.md scope; document memory (catalog seed)

- id: taxonomy
  ask: Do you have a preferred taxonomy and naming conventions?
  type: text
  default: file-safe slugs and the duplicate-suffix rule (§29); propose a taxonomy from the first cataloging pass
  skippable: yes
  when: always
  captures: document memory (taxonomy and naming conventions)

- id: file-op-gate
  ask: Confirm that moves, renames, archiving, and deletes are proposed, never acted on, without Proceed.
  type: boolean
  default: yes
  skippable: yes
  when: always
  captures: document-config.md approval boundaries (§3.2, §30)
```

## Update Interview

No questions — no migration required at this release.
