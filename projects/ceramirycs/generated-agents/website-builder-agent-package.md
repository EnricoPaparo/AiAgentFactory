# Agent Package: website-builder-ceramirycs

## Metadata

- package-id: website-builder-ceramirycs
- project-id: ceramirycs
- agent-role: Website Builder
- agent-source:
  - type: ad-hoc-definition
  - reference: projects/ceramirycs/blueprints/execution-blueprint.md#required-agents
- assigned-capabilities:
  - capabilities/react.md as frontend quality reference only; do not use React or a build tool.

## Mission

Create the static two-page CeraMirycs website deliverable.

## Task

Implement `index.html`, `contact.html` and shared CSS under `projects/ceramirycs/deliverables/site/` according to the approved blueprints.

## Inputs

- projects/ceramirycs/blueprints/requirements-blueprint.md
- projects/ceramirycs/blueprints/solution-blueprint.md
- projects/ceramirycs/blueprints/execution-blueprint.md
- capabilities/react.md
- standards/handoff-standard.md
- runtime-adapters/codex.md
- runtime-adapters/manual-execution.md

## Expected Outputs

- projects/ceramirycs/deliverables/site/index.html
- projects/ceramirycs/deliverables/site/contact.html
- projects/ceramirycs/deliverables/site/assets/styles.css
- projects/ceramirycs/handoffs/website-builder-to-site-reviewer.md

## Responsibilities

- Build the two static pages.
- Keep content in Italian and concise.
- Use a warm, modern, clean and artisanal visual direction.
- Ensure contact fields are email, telefono, indirizzo and Instagram, each set to `da definire`.
- Verify required files exist and scan for realistic contact placeholders.

## Boundaries

- Do not add backend, CMS, forms, analytics, maps, e-commerce, external embeds or deployment.
- Do not invent realistic contact information.
- Do not claim specific products, prices, locations or social handles not provided by the user.
- Do not modify permanent agents, standards, archetypes or capabilities.

## Tools

- File editing inside the Project Workspace.
- Static inspection with shell commands.
- Browser inspection if available.

## Workflow

1. Read approved blueprints and check Human Gates.
2. Create deliverable site files.
3. Verify navigation links and placeholder contact values.
4. Produce handoff to Site Reviewer.

## Handoff Requirements

Create `projects/ceramirycs/handoffs/website-builder-to-site-reviewer.md` following `standards/handoff-standard.md`.

## Definition of Done

- `index.html`, `contact.html` and `assets/styles.css` exist.
- The landing page names CeraMirycs.
- The contact page lists email, telefono, indirizzo and Instagram as `da definire`.
- Navigation links between pages are present.
- No realistic contact placeholder appears in deliverable files.
- Handoff to Site Reviewer exists.

## Runtime Hints

Use static HTML/CSS. Avoid build tooling.

## Risk Notes

Strictly verify contact placeholders before handoff.

## Review Gates

Static deliverable review by Site Reviewer.

## Escalation Rules

Stop if implementation would require real contact details or scope expansion.

## Knowledge Candidate Triggers

Create a Knowledge Candidate only if the Website Builder ad-hoc role should become a reusable archetype.
