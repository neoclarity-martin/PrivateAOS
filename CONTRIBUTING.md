# Contributing to the OpenAOS Factory

Thank you for your interest in improving the **OpenAOS Factory**. Contributions follow the same governance model the factory enforces for its own users: **every change flows through the design specification first.**

If you are new to contributing on GitHub, see [Contributing to a project](https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-a-project).

---

## The design spec is the single source of truth

The canonical source of truth for **OpenAOS** is `design-spec/openaos-design-specification.md` and associated spec files. They record every design decision made during development of **OpenAOS**: the governance model, the permission levels, the folder schema, the builder section structure, agent responsibilities and boundaries, workflow definitions, escalation rules, and the framework-vs-instance layout. **If the spec and a builder file ever disagree, the spec wins.**

Because everything is generated from this one canonical spec, the design, the docs, and the implementation can't quietly drift apart. Keeping that discipline is what makes outside contribution practical — and it's why **only pull requests for the design spec will be considered.**

---

## Active areas of development

Active development is going on in these areas:

- **Agents.** Improving and extending the behavior of existing agents as well as adding new, complementary agents.
- **User Experience.** Improving the user experience from initial AOS setup through to all interactions with the AOS and its agents.
- **Documentation.** Improving both user documentation and contributor documentation.

---

## How to contribute

There are two ways to contribute to the **OpenAOS** project.

### Submitting a suggestion or reporting a bug

Use the built-in Feedback Agent to report a bug or offer a suggestion for improvement. This will send an email to the project team. Simply say "I want to report a bug" or "I want to make a suggestion" along with the details of your feedback.

### Submitting a pull request to the repo

If you're an AI developer, you can contribute directly to the **OpenAOS** project through a GitHub pull request. Here's the general sequence of events.

1. Fork the repository on GitHub, then clone your fork into a local repo.
2. Create a new development branch off `main` in your local repo.
3. Make changes to the design spec and related design documents. The best way to do this is to collaborate with Claude. Otherwise it's very difficult to avoid drift and keep all the moving parts in sync. For heavy design work it's best to use Opus 4.8 with high effort or Fable 5 with low effort.
4. **OpenAOS** includes a runbook that defines the review process as well as the build processes for both the factory and the plug-in. Follow this sequence:
   - **"Using the runbook, conduct a Design Readiness Review."** This workflow loops until the design spec passes all the quality review gates.
   - **"Using the runbook, build the factory."** This checks to make sure the design review was successful and then creates an instance of the 
     `/aos-factory` in the project root folder. If an instance is already in the `/aos-factory` folder, this workflow will update it. 
   - **"Using the runbook, build the plugin."** This checks for a valid factory instance in the `/aos-factory` folder, then uses that instance to package the plugin in the folder `/claude-plugin/aos-factory`. If a plugin already exists, this workflow will update it.

5. Test your changes and iterate as needed.
6. Commit your changes and push your development branch to your fork on GitHub.
7. Open a pull request from your branch against `main`. **Only pull requests for the design spec will be considered.**

**What happens after you submit**

Opening a pull request doesn't change `main` — it only proposes your change. Nothing merges until a maintainer reviews it, and your branch stays under your control the whole time. A maintainer will review the diff, run the automated checks, and check out your branch to test it before deciding. If adjustments are needed, they may ask you to push more commits to the branch or tweak it themselves, and a change that needs longer to stabilize may be routed to an integration branch first. Your work only reaches `main` once it has been reviewed and tested and a maintainer merges the pull request.

---

## What not to do

Do not directly modify the build artifacts in `/aos-factory` folder or the `/claude-plugin/aos-factory` folder. These changes will not be accepted into the repo. All modifications must originate with the design spec.

## Questions

For questions, or to discuss larger architectural changes before drafting spec language, open an issue on GitHub.
