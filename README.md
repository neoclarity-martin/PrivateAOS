# OpenAOS

| ![OpenAOS — AI for the rest of us](https://repository-images.githubusercontent.com/1263423041/c7102ffa-3f2b-4d04-ac2e-2e17a0f31beb) | AI for the rest of us<br /><br />Realize the full potential of Claude Cowork with a fully-governed team of AI Agents that you build through conversation.<br /><br />No technical experience required |
| ------------------------------------------------------------ | ------------------------------------------------------------ |

*Lovingly built by humans with Claude in the loop*

## Why This Exists

Claude by Anthropic is one of the most powerful and popular generative AI tools on the planet. Claude Cowork is a desktop app designed to make Claude more useful and accessible for non-technical users. Cowork gives you a powerful general-purpose platform: project memory, skills, subagents, plugins, scheduled tasks, and a permission system. What it deliberately doesn't give you is a framework for assembling these primitives into a trustworthy, coordinated team of agents. A non-technical person has no straightforward path from the generic platform (essentially a blank sheet) to a highly productive app tailored to the their specific needs. **OpenAOS** closes that gap. It lets anyone turn Claude Cowork into a purpose-built team of governed agents through an interview-style conversation. No settings to configure, no code to write. What's more, governance comes first, not as an afterthought. Every consequential action waits on a one-word human approval (`Proceed`), minimizing the risk of unintentional changes. And the entire system is generated from a single canonical specification, so the design, the docs, and the shipped code cannot quietly drift apart.

## Overview

**OpenAOS** builds and maintains an **Agentic Operating System (AOS)** instance. The AOS is a standardized personal or professional AI operating environment composed of specialized agents, workflows, memory files, templates, and configuration files that work together to create a complete agentic system. **OpenAOS** guides both technical and non-technical users through setup via a conversational interview, produces all files automatically once approved, and can add or rebuild individual agents at any time. Although this particular implementation is configured to run on Claude Cowork, with non-technical users in mind, the design spec is a portable artifact that can be rendered to run on Codex or any similar agentic platform.

**What is an Agentic Operating System?**

An Agentic Operating System (AOS) is not a piece of software you install. It's a structured workspace that gives a Large Languae Model (LLM) like Claude a persistent identity, a memory, and a set of specialized agents, each with clear responsibilities, boundaries, and escalation rules. The AOS consists of a collection of markdown files and HTML templates designed to work efficiently together. Once built, Claude reads the "bootstrap" file AGENTS.md at the start of every session and then reads additional AOS files based on the nature of the request. This structure causes Claude Cowork to behave consistently across conversations, route tasks to the right agent, coorindate multiple agents, remember context, and follow well defined rules.

### What Makes OpenAOS Unique?

**OpenAOS** contributes a distinct combination of innovations.

**1. A factory that builds operating systems, not just agents.** "Agent factory" tooling already exists (Microsoft's Agent Factory, Mozilla's "agent-factory", Oracle's Private Agent Factory, research like MetaGPT and Automated Design of Agentic Systems). All of them generate *individual agents* or *multi-agent workflows*. **OpenAOS** instead generates a complete, governed **Agentic Operating System** (workspace, persistent identity, shared memory, governance layer, and a coordinated agent team). Here's the difference: **OpenAOS** is a factory-of-systems, not factory-of-agents. In this way, it offers a complete solution for non-technical users.

**2. Mandatory governance agents that bootstrap the system.** "Governance-first" is now an emerging, named paradigm, but the literature treats governance as a *layer* or *control plane* bolted around the agents. This project makes governance **five required agents** (security, memory, coordination, review, and upstream feedback) that *must* be instantiated before any productive agent exists. Governance isn't a wrapper; it's a foundational component for every AOS instance built by **OpenAOS**.

**3. The design spec is the single source of truth.**  The **OpenAOS** design spec is used to render the `aos-factory`, a specialized set of agents that work with you to build your own custom AOS. The design spec then packages the rendered factory into a Claude plugin that you can easily install and use.  to build the This factory follows a well defined structure and set of rules laid out in the design spec. These include the governance model, the permission levels, the folder schema, the builder section structure, agent responsibilities and boundaries, workflow definitions, and escalation rules. The design spec his its own review process to ensure consistency and safety and the plugin is built from the factory.

Individually, each idea has neighbors in the field. The **combination** of a factory that generates a governed AOS instance, governance implemented as required agents, all generated from a single canonical spec, and aimed at non-technical users, is one we have not found assembled in any single existing project. That combination is the contribution.

### How OpenAOS Relates to Claude Cowork

**OpenAOS** is not a replacement for Claude Cowork. Rather, **OpenAOS** complements and extends it. Cowork provides the primitives and stays general-purpose by design. **OpenAOS** turns those primitives into a specific, governed system shaped to the user's needs.

The AOS built by **OpenAOS** is not a replacement for the Claude Cowork. Rather, the AOS complements and extends it. Cowork provides the primitives and stays general-purpose by design. The AOS turns those primitives into a specific, governed system shaped to the user's specific needs.

**Where it overlaps.** An AOS built by **OpenAOS** reuses Cowork's own primitives rather than replacing them: project memory (the `memory/` folder is a structured application of it, not a new mechanism), skills/subagents (agents are markdown instruction files invoked through Cowork's existing skill/subagent execution), scheduled tasks (the daily/weekly/monthly operating rhythms are Cowork's scheduler, pre-wired to specific cadences), the permission system (the three-level model and tool-access matrix sit on top of Cowork's own approval gating), and plugins (**OpenAOS** itself ships and installs as a standard Cowork plugin).

**Where it complements.** Cowork has no concept of agents that must exist before productive work happens, no enforcement of single-responsibility boundaries between skills, no unified approval gate beyond its own built-in safeguards, no notion of a canonical spec used to generate the running system, and no built-in cadence for documenting or reviewing itself. The Factory adds all of these: the five required governance agents, Chief-of-Staff-enforced single responsibility, the `Proceed` gate layered on top of Cowork's own safety checks, spec-driven regeneration, and the self-documenting/self-improving review rhythms.

In short, Cowork supplies the engine; the AOS is a custom-built vehicle powered by that engine. **OpenAOS** reuses Cowork's mechanisms whenever possible and adds only the governance and non-technical usability to realize Cowork's full potential.

**Using OpenAOS on Claude Code**

Although Claude Code is not as user friendly as Claude Cowork, it has additional capabilities for power users. Claude Code not only runs **OpenAOS**, it's also the preferred development environment for OpenAOS contributors. For this reason, instructions are provided for both Claude Cowork and Claude Code.

------

## Prerequisites

The **OpenAOS** implementation included with this repo requires:

- **The Claude Desktop application:** Required to run [Claude Cowork](https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork).
- **A Claude subscription:** Also required to run Claude Cowork. Claude Pro is the minimum subscription level, and it's sufficient for most uses of **OpenAOS**. See the [Claude plans page](https://claude.com/pricing) for the available options.
- **An active Internet connection:** Required by the Claude Desktop application.

---

## Quick Start

The fastest way to get started is to use the OpenAOS Plugin. Here's how: 

- [Quick Start for Claude Cowork](claude-plugin/quick-start-claude-cowork.md)
- [Quick Start for Claude Code](claude-plugin/quick-start-claude-code.md)

---

## Key Features

**Governance-first architecture.** Every AOS includes five required governance agents that must be set up before any productive agents are added. These agents own the system's safety, memory, coordination, quality, and upstream feedback, not any one task domain.

**Three-level permission model.** Actions are classified as Level 1 (safe autonomous: the agent may act without asking), Level 2 (approval-required: the agent must describe the action and ask the user to type `Proceed`), or Level 3 (prohibited: the agent must not do this at all). The global tool-access matrix is the authoritative source for permissions and overrides any agent-level setting in the event of a conflict.

**Non-destructive by default.** No agent deletes, overwrites, renames, moves, or bulk-modifies files without explicit approval — when in doubt it creates a new file, appends to a log, or asks. Every Level 2 action requires the user to type exactly `Proceed`; anything short of that exact word is a hold. This sits on top of the platform's own safeguards by design: Cowork and Code already gate consequential actions, but both will sometimes edit files before you're ready, so the `Proceed` gate guarantees nothing changes until you're satisfied and gives you a clean point to abandon a direction before anything is committed.

**Single Responsibility Principle.** Each agent has a well-defined purpose and set of responsibilities. **OpenAOS** ensures that responsibilities don't overlap. For instance, the Chief of Staff agent coordinates and routes without taking on any other responsibilities.

**Scheduled, recurring work.** Agents don't only act when prompted. They can also run on a cadence. Each AOS includes daily, weekly, and monthly operating rhythms: a daily start-of-day briefing and inbox pass driven by the Chief of Staff, plus a weekly review and a monthly health check, user-guide refresh, and goal-alignment retrospective, all owned by the Review Agent. You approve the schedule once. The system maintains the rhythm so routine work happens on its own.

## Key Benefits

**Easy setup.** You don't need any specialized technical knowledge to build your own AOS. You simply create a new Claude Cowork project and then issue the command to "Build an AOS". **OpenAOS** then walks you through an interview in plain English. It guides, you talk, it builds.

**Easy to modify and update.** You can add agents at any time. Just say "Add an agent" to be given a selection of uninstalled agents. Also, as **OpenAOS** evolves, you can update your plugin and use it, in turn, to update your AOS for the latest features.

**You can trust it with real work.** Governance comes first, not as an afterthought. Before any productive agent is added, five governance agents (security, memory, coordination, quality review, and upstream feedback) are already in place. The system never deletes, overwrites, or moves your files on its own. Anything consequential waits for you to type one word: `Proceed`.

**It's built for non-technical people.** Using your AOS requires no command grammar to memorize. You trigger things by plain intent ("Start my day", "Process my inbox", etc.).

**It documents and improves itself.** Every system generates its own plain-language user guide, and a built-in review agent ensures that your AOS stays healthy and aligns itself with your goals. In other words, it gets better with use.

**It's designed to be forked and extended.** Everything is plain markdown built from standardized schemas. The whole system is generated from one canonical design spec, so the design, the docs, and even this README can't quietly drift apart. That same discipline is what makes outside contribution easy.

**It's portable.** Tuned for Claude Cowork, but the same design-spec can be configured to work with other platforms, such a Codex. However, this requires some technical know-how.

---

## Available Agents

| Agent                                 | Role                                                         |
| ------------------------------------- | ------------------------------------------------------------ |
| **Chief of Staff Agent** *(required)* | Coordinates, routes, prioritizes, and resolves conflicts across agents; joint owner of the AOS Workspace router |
| **Security Agent** *(required)*       | Owns permission rules, approval requirements, access boundaries, the tool-access matrix, and safety checks; the escalation target for all permission, access, and privacy questions |
| **Memory Agent** *(required)*         | Owns shared memory structure, memory hygiene, preference capture, and cross-agent memory routing |
| **Review Agent** *(required)*         | Owns retrospectives, system improvement, the review cadence, decision audits, AOS refinement, and the AOS User Guide |
| **Feedback Agent** *(required)*       | Owns the upstream feedback channel: captures bug reports and enhancement proposals locally, then submits them to **OpenAOS** after scrubbing and approval |
| Inbox Agent                           | Triages incoming communications and drafts responses; promotes items into other agents' domains but owns none of them |
| Calendar Agent                        | Owns scheduling: reading availability, proposing times, and creating or changing calendar events under approval |
| Task Agent                            | Owns task and commitment tracking: capturing, prioritizing, and closing out tasks from inbox items, projects, and direct requests |
| Document Agent                        | Owns document management: filing, organizing, and retrieving documents and reference material across the AOS |
| Automation Agent                      | Owns automation and tool-use: scripting, integrations, and recurring automated actions on behalf of other agents |
| Project Manager Agent                 | Owns project coordination: briefs, plans, milestones, stakeholders, and cross-task tracking for active projects |
| Research Agent                        | Owns research: gathering, synthesizing, and sourcing information for projects, decisions, and learning |
| Writing Agent                         | Owns long-form content and drafting: documents, posts, and written deliverables distinct from message replies |
| Tutor Agent                           | Owns learning: structuring material into lessons, tracking progress, and supporting study or skill-building goals |
| Personal CRM Agent                    | Owns contacts: relationship context, communication preferences, and collaboration notes about people |

At least one optional productive agent must be added before the AOS setup is considered complete. A good starting set is the **Inbox**, **Calendar**, **Task**, **Document**, and **Automation** agents. Additional agents can be added later if needed.

## Repository Structure

```
OpenAOS/                         ← project root
│
├── CLAUDE.md                    ← session-start instructions for Claude
├── AGENTS.md                    ← Proceed gate definition, basic routing; pulled in by CLAUDE.md
├── README.md                    ← This document
├── CONTRIBUTING.md              ← Instructions for those interested in contributing to the project
├── LICENSE                      ← MIT license
│
├── design-spec/                 ← canonical design specification document set
│   ├── openaos-design-specification.md  ← canonical design spec
│   ├── openaos-packaging-runbook.md    ← build/regeneration runbook
│   └── openaos-revision-history.md      ← spec revision history
│
├── aos-factory/                 ← factory source (not an AOS instance)
│   ├── build-aos.md             ← entry-point pointer to the master builder
│   ├── builder-changelog.md
│   ├── agent-catalog.yaml       ← rendered catalog of all agents (§7A.4)
│   ├── aos-interviews.md        ← AOS-level setup interview (§7C/§12.1)
│   ├── agent-specs/             ← 15 agent spec folders, each with profile.md + interviews.md
│   └── builders/                ← build-aos.md (master builder) + build-agent.md (generic build engine)
│
└── claude-plugin/               ← packaged plugin (for Claude Cowork users)
    └── aos-factory/
        ├── .claude-plugin/
        │   └── plugin.json      ← plugin manifest
        ├── README.md
        ├── builder-changelog.md
        ├── skills/              ← 2 SKILL.md files: build-aos and build-agent
        └── templates/           ← starter files to copy into the workspace
```

---

## Technical Overview

**Design philosophy.** **OpenAOS** applies the **Single Responsibility Principle** at every level: each agent owns exactly one domain, and coordination is the Chief of Staff's job rather than being absorbed into a catch-all central agent. The governance layer (the five required agents) is mandatory because safety, memory, coordination, quality review, and upstream feedback must exist before any productive work happens. Optional productive agents are additive and replaceable.

**`CLAUDE.md` and `AGENTS.md`.** These two files are the load-bearing wiring of the system. `CLAUDE.md` is read by Claude at the start of every session; it sets Planning mode behavior and pulls in `AGENTS.md`. `AGENTS.md` carries the governance-removal hard rule and the factory-vs-instance guard: before running any workflow, determine whether a request targets **OpenAOS** or the generated AOS instance, asking rather than guessing when ambiguous. An example copy of `CLAUDE.md` ships under `claude-plugin/aos-factory/templates/` and should be copied to the workspace root after install.

**Builder schema.** The builder files (`build-aos.md` and the generic `build-agent.md`) follow a standardized YAML front matter schema (`title`, `file_type`, `builder_version`, `schema_version`, `created_date`, `last_updated`, `status`, `compatible_aos_versions`, `requires_approval_for_overwrite`) and a common markdown section structure: Builder Purpose, When to Use, Builder Operating Mode, Interview Flow, Discovery Questions, Recommended Defaults, Configuration Decisions, and Output Files. This consistency allows **OpenAOS** to be extended with new agents — via the rendered `agent-specs/` — without redesigning the builder format.

**What a built instance looks like.** When `build-aos` completes an authorized build, it creates a folder with the user's chosen AOS name containing:

```
[aos-name]/
  agents/          ← one subfolder per installed agent
  workflows/       ← cross-agent workflow files
  memory/          ← shared memory and user profile
  projects/        ← active project folders
  logs/            ← decision and activity logs
  templates/       ← reusable document templates
  configs/         ← global permissions, tool-access matrix, preferences
  docs/            ← the AOS User Guide and build documentation
  inbox/
    processed/
  archive/
```

**Versioning.** Builder and plugin versions are tracked in `claude-plugin/aos-factory/builder-changelog.md`. Instance-level changes belong in each instance's own `/logs/change-log.md`.

---

## OpenAOS Design Specification

The canonical source of truth for **OpenAOS** is `design-spec/openaos-design-specification.md`. It records every design decision made during **OpenAOS**'s development: the governance model, the permission levels, the folder schema, the builder section structure, agent responsibilities and boundaries, workflow definitions, escalation rules, and the framework-vs-instance layout. If the spec and a builder file ever disagree, the spec wins.

The spec is the correct starting point for any change to **OpenAOS** itself. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full contribution workflow.

---

## Maintainer and Project Status

**OpenAOS** is built and actively maintained by Martin Danner, founder of neoClarity, with decades in software engineering, technical training, and IT management. neoClarity is a human-centered AI learning community focused on making capable AI accessible to non-technical professionals. More info at [https://neoclarity.ai](https://neoclarity.ai)

The project is under active development with ongoing commits on `main`, a published architecture and a spec-driven contribution model, and labeled good-first-issues for new contributors. The reference **OpenAOS** build was created with Claude Opus 4.8 and is designed to be rebuilt as newer models ship. Issues and design-spec pull requests are welcome.

## Contributing

Contributions follow the same governance model **OpenAOS** enforces for its own users: every change flows through the design specification first, and **only pull requests for the design spec will be considered.** See **[CONTRIBUTING.md](CONTRIBUTING.md)** for the full workflow, including how to propose a change, add a new agent builder, and what not to edit directly.
