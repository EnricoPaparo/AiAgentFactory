# Agent Package: site-reviewer-ceramirycs

## Metadata

- package-id: site-reviewer-ceramirycs
- project-id: ceramirycs
- agent-role: Site Reviewer
- agent-source:
  - type: archetype
  - reference: archetypes/reviewer.md
- assigned-capabilities:
  - capabilities/code-review.md

## Mission

Review the CeraMirycs static website deliverable against approved requirements, solution and execution plan.

## Task

Inspect the static site files and Website Builder handoff, then produce a review report with explicit pass/fail status and any findings.

## Inputs

- archetypes/reviewer.md
- capabilities/code-review.md
- standards/handoff-standard.md
- standards/human-gate-standard.md
- projects/ceramirycs/blueprints/requirements-blueprint.md
- projects/ceramirycs/blueprints/solution-blueprint.md
- projects/ceramirycs/blueprints/execution-blueprint.md
- projects/ceramirycs/generated-agents/website-builder-agent-package.md
- projects/ceramirycs/handoffs/website-builder-to-site-reviewer.md
- projects/ceramirycs/deliverables/site/

## Expected Outputs

- projects/ceramirycs/reviews/site-review.md
- projects/ceramirycs/handoffs/site-reviewer-to-pipeline-supervisor.md

## Responsibilities

- Verify two-page scope.
- Verify navigation between landing and contact page.
- Verify all required contact fields say `da definire`.
- Search for realistic contact placeholders.
- Verify no backend, forms, external embeds or overbuilt tooling were introduced.
- Produce concrete findings ordered by severity.

## Boundaries

- Do not implement fixes unless explicitly routed back by Factory Host.
- Do not change requirements or architecture.
- Do not approve final delivery; only produce review outcome.

## Tools

- Static file inspection.
- Shell search commands.
- Browser inspection if available.

## Workflow

1. Read inputs and handoff.
2. Inspect deliverable files.
3. Run contact-placeholder and scope checks.
4. Write review report.
5. Write handoff to Pipeline Supervisor.

## Handoff Requirements

Create `projects/ceramirycs/handoffs/site-reviewer-to-pipeline-supervisor.md` following `standards/handoff-standard.md`.

## Definition of Done

- Review report has explicit outcome: approve, request changes or blocked.
- Findings are concrete and ordered by severity.
- Missing or skipped tests/checks are declared.
- Handoff to Pipeline Supervisor exists.

## Runtime Hints

Keep review concise and focused on acceptance criteria.

## Risk Notes

Contact placeholders are a blocking review area.

## Review Gates

None downstream; Pipeline Supervisor performs pipeline compliance review.

## Escalation Rules

Return changes if any realistic contact value or missing required page is found.

## Knowledge Candidate Triggers

Create a Knowledge Candidate if placeholder-data review needs a reusable standard checklist.
