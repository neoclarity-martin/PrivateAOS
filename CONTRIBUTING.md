# Contributing to OpenAOS

Thank you for your interest in improving **OpenAOS**. Contributions follow the same governance model OpenAOS enforces for its own users: **every change flows through the design specification first.**

If you are new to contributing on GitHub, see [Contributing to a project](https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-a-project).

---

## The design spec is the single source of truth

The canonical source of truth for **OpenAOS** is `design-spec/openaos-design-specification.md` and its companion files (the packaging runbook, the workflow catalog, the controlled vocabularies, the file skeletons, the setup interview, and the use-case builder specs under `design-spec/workflow-specs/`). They record every design decision: the governance model, the permission levels, the workspace schema, the builder and refinement engine contracts, the governance workflows, and the plugin packaging rules. **If the spec and a generated artifact ever disagree, the spec wins.**

Because everything is generated from this one canonical spec, the design, the docs, and the shipped plugin can't quietly drift apart. Keeping that discipline is what makes outside contribution practical — and it's why **only pull requests for the design spec will be considered.**

---

## Active areas of development

- **Workflows.** Improving the five use-case builder specs and the general AI-pattern library behind the custom builder.
- **User Experience.** Improving the experience from setup through building, running, and refining workflows.
- **Documentation.** Improving both user documentation and contributor documentation.

---

## How to contribute

### Submitting a suggestion or reporting a bug

Use the built-in feedback workflow: say "I want to report a bug" or "I want to make a suggestion" along with the details. Your feedback is scrubbed of personal details, previewed to you, and emailed to the project team only when you type `Proceed`.

### Submitting a pull request to the repo

1. Fork the repository on GitHub, then clone your fork into a local repo.
2. Create a new development branch off `main`.
3. Make changes to the design spec and related design documents. The best way to do this is to collaborate with Claude — otherwise it's very difficult to avoid drift and keep the moving parts in sync. For heavy design work it's best to use Opus 4.8 with high effort or Fable 5 with low effort.

   *Optional:* if starting in a large specification document is the hard part, you can prototype directly in `claude-plugin/openaos/skills/` instead. Editing a `SKILL.md` is concrete and small; §12 of the spec is not. Then say **"Using the runbook, sync the design spec with the plugin."** (runbook §36.3) to draft the matching spec change. **Review and edit that draft — it is a starting point, and you are the author of the spec language you submit.** A prototype edit that conflicts with a fundamental design tenet is not reflected; the sync stops and tells you which tenet, so you can decide.
4. Follow the runbook (`design-spec/openaos-packaging-runbook.md`):
   - **"Using the runbook, conduct a Design Readiness Review."** Loops until the spec passes all review gates, including the repo validators.
   - **"Using the runbook, generate the plugin."** Regenerates `claude-plugin/openaos/` from the reviewed spec. This is always the last runbook step, so the plugin in your PR is generated from the spec you're proposing.
5. Test your changes and iterate as needed.
6. Commit, push your branch to your fork, and open a pull request against `main`. **Only pull requests for the design spec will be considered.**

**What happens after you submit**

Opening a pull request doesn't change `main` — it only proposes your change. A maintainer will review the diff, run the automated checks, and test your branch before deciding. If adjustments are needed, they may ask you to push more commits or tweak the branch themselves; a change that needs longer to stabilize may be routed to an integration branch first. Your work reaches `main` once it has been reviewed, tested, and merged by a maintainer.

---

## What not to do

Do not *submit* direct modifications to the generated plugin in `claude-plugin/openaos/`. Prototyping there is fine and even encouraged if it's the easier place to start (see step 3 above) — but what you propose is a spec change, and the plugin in your pull request must be byte-identical to what the spec generates. Automated checks assert this on every pull request, so a branch that skips the round trip fails before a maintainer looks at it.

The governance layer of the design (the `Proceed` gate, the governance config, and the five governance workflows) is not removable; proposals that remove or weaken it will not be considered.

## Questions

For questions, or to discuss larger architectural changes before drafting spec language, open an issue on GitHub.
