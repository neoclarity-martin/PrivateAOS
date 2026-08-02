# OpenAOS

| ![OpenAOS — AI for the rest of us](https://repository-images.githubusercontent.com/1263423041/c7102ffa-3f2b-4d04-ac2e-2e17a0f31beb) | AI for the rest of us<br /><br />Build the most useful, most user-friendly AI workflow for each of your core use cases — through conversation, safe by default.<br /><br />No technical experience required |
| ------------------------------------------------------------ | ------------------------------------------------------------ |

*Lovingly built by humans with Claude in the loop*

## Why This Exists

Claude Cowork makes Claude accessible to non-technical users — but it leaves them on their own to turn that access into workflows that are actually good: well-designed, tailored to their situation, and safe to run against their real files. 

**OpenAOS** closes that gap. Its purpose is to collaboratively build the best possible workflow for each of the things you actually do, through a guided interview that embeds AI best practices you don't have to know; to let you refine any workflow just as easily; and to keep all of it safe by default — nothing destructive happens without the one word `Proceed` — and improving over time, with an easy channel to send feedback back to the project team.

## What It Is

**A generative core, guarded — nothing more.** The whole system is exactly three things:

1. **Use-case workflow builders** — guided interviews that co-design a tailored, best-practice workflow for each core use case:

   | Workflow | Purpose |
   |---|---|
   | Inbox triage | Classify, route, and act on inbox items |
   | Research assistant | Scoped, source-disciplined research |
   | Writing assistant | Drafting/editing keyed to your voice |
   | Learning assistant | Guided learning with understanding checks |
   | Organizer / declutter | File cleanup — inbox triage for files |

   Plus a **custom builder** ("design my own") that co-designs brand-new workflows for whatever *you* do to create value — OpenAOS is not limited to the use cases we anticipated.

2. **Workflow refinement** — the same collaborative interview, pointed at an existing workflow: say what's not working, see a before/after preview, approve the change.

3. **Guardrails** — a governance config (the `Proceed` gate, permission model, memory boundaries) and five governance workflows (daily startup, end of day, weekly review, monthly review, feedback) that make the workflows trustworthy. The governance layer is installed with every workspace and is not removable.

## How It Works

OpenAOS ships as a single Claude plugin generated directly from its design specification. Install it, say **"set up openaos"**, answer a few questions about your situation, and approve the preview. Setup scaffolds your workspace:

```text
/[your workspace]
├── CLAUDE.md, AGENTS.md      ← session entry + standing instructions
├── governance/governance.md  ← the standing rules (Proceed gate, permissions, memory)
├── workflows/                ← your workflows: five governance + the ones you build
├── memory/                   ← durable facts, preferences, people, decisions
├── logs/                     ← decision log, change log, feedback log
├── templates/                ← report, decision, approval, memory templates
├── docs/user-guide.html      ← your plain-language manual, kept current
├── outputs/  inbox/  archive/
```

Then build workflows as you need them ("build a workflow"), refine them when they should fit better ("refine my inbox triage workflow"), and let the governance rhythms keep everything clean, remembered, and aligned with your goals.

**The one rule:** `Proceed` is the only exact-word command in the system. Nothing is deleted, overwritten, moved, sent, published, or spent without it. Everything else is just conversation.

## Design Principles

- **The design spec is the single source of truth.** Everything — the skills, the governance content, the docs — is generated from `design-spec/openaos-design-specification.md`. If they ever disagree, the spec wins, and the artifact is corrected.
- **Governance before productivity.** The guardrails are scaffolded before any productive workflow exists, and cannot be removed.
- **Non-destructive and approval-gated by default.** When in doubt, the system copies, appends, or asks.
- **Value first.** Workflows are authored for maximum usefulness; efficiency concerns never compromise quality.
- **Built for non-technical users, portable by design.** The spec is a portable artifact; this implementation targets Claude Cowork and Claude Code.

## Repository Layout

```text
design-spec/                      ← the canonical spec + companion data files
├── openaos-design-specification.md
├── openaos-packaging-runbook.md
├── openaos-revision-history.md
├── workflow-catalog.yaml, vocabulary.yaml, file-skeletons.yaml (+ schemas)
├── setup-interview.md
└── workflow-specs/[slug]/spec.md ← the five use-case builder specs
scripts/                          ← repo CI validators
claude-plugin/openaos/            ← the generated plugin (skills, content, templates)
```

## Contributing

Contributions follow the same governance model OpenAOS enforces for its own users: every change flows through the design specification first, and **only pull requests for the design spec will be considered.** See **[CONTRIBUTING.md](CONTRIBUTING.md)**. To report a bug or suggest an improvement from inside OpenAOS, just say "I want to report a bug" — the feedback workflow scrubs, previews, and (on `Proceed`) sends it to the team.

## License

See [LICENSE](LICENSE).
