---
title: OpenAOS Setup — Interview
file_type: interview_script
slug: setup-openaos
openaos_version: 3.2.0
---
# OpenAOS Setup — Interview

The setup-flow interview, owned by the `setup-openaos` skill (§8.1 step 1)
and executed once after install. Question schema: §7B.2. Answers feed the
scaffold preview (§8.1 step 2); nothing is written before `Proceed`.

## Setup Interview

Begin by displaying this welcome message: "Welcome to OpenAOS. Together we
will be creating a personalized set of specialized workflows known as an
Agentic Operating System. A few quick questions, then I'll show you exactly
what will be set up — nothing is created until you approve it. Type `Proceed`
to continue."

Wait for the user to type exactly `Proceed` before asking the first question
(§8.1 step 1; this acknowledgment gate is distinct from the §3.1 write gate,
which still governs the scaffold itself). Then conduct this interview:

```yaml
- id: workspace-root
  ask: Which folder should be your openaos workspace? Everything openaos creates will live inside it.
  type: text
  default: the current folder, named explicitly for confirmation
  skippable: no
  when: always
  captures: the workspace root the §4 folder structure is scaffolded into

- id: work-platform
  ask: Which platform do you do most of your work in?
  type: choice
  options: [Google Workspace, Microsoft 365, Dropbox, Something else or not sure]
  default: Something else or not sure
  skippable: yes
  when: always
  captures: a work-platform seed in /memory/user-profile.md (§20.1), read by
    build-workflow during situation elicitation (§12.1(a)) to word generated
    steps in the user's own tool vocabulary

- id: rhythm-optin
  ask: openaos includes optional check-in rhythms — a short daily startup and wrap-up, a weekly review, and a monthly health check. Which would you like to start with?
  type: choice
  options: [all of them, daily only, weekly and monthly only, none for now]
  default: all of them
  skippable: yes
  when: always
  captures: which §17 governance workflows are scheduled (all five files are always installed; this sets only the active cadences)

- id: memory-seeds
  ask: Any people, tools, or preferences I should remember from the start?
  type: text
  default: none — seed empty, never fabricate
  skippable: yes
  when: always
  captures: initial entries in the §20.1 memory files (each shown in the scaffold preview)

- id: use-case-selection
  ask: Which workflows would you like to build first? (You can build any of these later, or design your own.)
  type: choice
  options: [Inbox triage, Research assistant, Writing assistant, Learning assistant, File organizer, Design my own, None yet]
  default: none — zero selections is valid (§8.1 step 4)
  skippable: yes
  when: always
  captures: the build-workflow handoffs run after scaffolding (§8.1 step 4)
```

Rules: `rhythm-optin` never uninstalls a governance workflow — all five are
always scaffolded (§16.1 non-removable layer); the answer only sets which
cadences are scheduled, and any of them can be started later.
`use-case-selection` may take multiple choices; each selected use case (or
"Design my own") becomes one `build-workflow` session after the foundation
is approved and created.

The `work-focus` question was removed in this §36.3 cycle. Its two captures are now
sourced as follows: the §8.1 use-case menu is presented in
`workflow-catalog.yaml` order rather than reordered by stated focus, and the
`/memory/user-profile.md` seed is built from `memory-seeds` plus the
`work-platform` preference. Neither capture is silently dropped, and
nothing is inferred about the user's work that they did not state.

## Update Interview

No questions — a plugin update proposes per-file diffs (§14.4) rather than
re-interviewing.
