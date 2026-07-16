---
title: AOS Setup — Interviews
file_type: interview_script
slug: build-aos
spec_version: 2.4.2
---
# AOS Setup — Interviews

The AOS-level setup interview, owned by `build-aos.md` (§12.1) and executed
during initial AOS setup (§9.3). Schema and execution rules: §7C.

## Initialization Interview

Begin by displaying this welcome message: "Thank you for choosing to install OpenAOS. We'll start by asking a few simple questions." Then, conduct this interview:

```yaml
- id: aos-purpose
  ask: What is this AOS for?
  type: choice
  options: [Personal Productivity, Project Management, Client Specific, Other]
  default: none
  skippable: no
  when: always
  captures: scope; proposed instance name; /aos-manifest.md

- id: aos-name
  ask: What should the AOS be named?
  type: text
  default: proposed from the stated purpose (file-safe slug, §29)
  skippable: yes
  when: always
  captures: instance root folder slug; /aos-manifest.md

- id: optional-agents
  ask: Which optional productive agents do you want first? At least one is required (§2.3, §7.2); the rest can be added later (§9.4).
  type: text
  default: recommend by the stated aos-purpose category — Inbox + Task + Calendar + Document for Personal Productivity, Project Manager + Task + Document for Project Management, Personal CRM + Task + Calendar for Client Specific; for Other, present the full §7.2 roster with no default
  skippable: no
  when: always
  captures: agent selection; /configs/agent-registry.md; /aos-map.md

- id: memory-seeds
  ask: Any known people, projects, tools, or preferences to seed memory with?
  type: text
  default: none — seed empty, never fabricate
  skippable: yes
  when: always
  captures: /memory global files initial entries

```

Purpose categories: Personal Productivity merges the former separate "work"
and "personal" answers, since neither carried distinct downstream behavior. If
the user selects Other, capture a short free-text description alongside it —
that description substitutes for the category name wherever purpose feeds
`aos-name`'s default slug (§29) and the /aos-manifest.md scope field.

## Update Interview

No questions — no migration required at this release.
