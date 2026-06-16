# Execution Blueprint: ceramirycs

## Requirements Source

projects/ceramirycs/blueprints/requirements-blueprint.md

## Solution Source

projects/ceramirycs/blueprints/solution-blueprint.md

## Execution Goal

Produce and verify a minimal two-page static website for CeraMirycs under `projects/ceramirycs/deliverables/site/`, preserving the warm modern artisan direction and ensuring every real contact field remains `da definire`.

## Required Agents

- Website Builder
  - source: ad-hoc-definition
  - motivation: no existing archetype precisely covers small static visual website implementation with strict placeholder-content rules.
  - responsibility: create the static website deliverable.
- Site Reviewer
  - source: archetype `archetypes/reviewer.md`
  - motivation: review output against requirements, solution blueprint, contact-placeholder constraint and local inspectability.
  - responsibility: produce review report and identify required fixes.
- Pipeline Supervisor
  - source: permanent agent `agents/pipeline-supervisor/pipeline-supervisor.md`
  - motivation: confirm workflow, handoffs, gates, review and deliverables before final human approval.
  - responsibility: produce final supervision report and open final delivery gate.

## Agent Inputs

- Website Builder:
  - projects/ceramirycs/blueprints/requirements-blueprint.md
  - projects/ceramirycs/blueprints/solution-blueprint.md
  - projects/ceramirycs/blueprints/execution-blueprint.md
  - capabilities/react.md only as frontend quality reference, not as a framework requirement
  - standards/handoff-standard.md
- Site Reviewer:
  - Website Builder handoff
  - projects/ceramirycs/deliverables/site/
  - projects/ceramirycs/blueprints/requirements-blueprint.md
  - projects/ceramirycs/blueprints/solution-blueprint.md
  - capabilities/code-review.md
  - standards/handoff-standard.md
- Pipeline Supervisor:
  - all project blueprints
  - all human gates
  - generated Agent Packages and handoffs
  - reviewer report
  - final deliverable files

## Agent Outputs

- Website Builder:
  - projects/ceramirycs/deliverables/site/index.html
  - projects/ceramirycs/deliverables/site/contact.html
  - projects/ceramirycs/deliverables/site/assets/styles.css
  - optional local decorative asset only if implemented as code or static file
  - projects/ceramirycs/handoffs/website-builder-to-site-reviewer.md
- Site Reviewer:
  - projects/ceramirycs/reviews/site-review.md
  - projects/ceramirycs/handoffs/site-reviewer-to-pipeline-supervisor.md
- Pipeline Supervisor:
  - projects/ceramirycs/reviews/pipeline-supervisor-report.md
  - projects/ceramirycs/human-gates/approve-final-delivery.md

## Workflow

1. Human Maintainer approves `approve-execution-plan`.
2. Knowledge Compiler generates temporary Agent Packages for Website Builder and Site Reviewer.
3. Website Builder executes its package using the Codex Runtime Adapter in the current conversation.
4. Website Builder creates the static site and handoff to Site Reviewer.
5. Site Reviewer executes its package and reviews the deliverable.
6. If review requests changes, return to Website Builder with bounded fixes.
7. Pipeline Supervisor reviews the full pipeline and deliverables.
8. Pipeline Supervisor opens `approve-final-delivery`.
9. Factory Host stops and requests human decision for final delivery.

## Handoffs

- Pipeline Designer to Knowledge Compiler:
  - condition: `approve-execution-plan` Approved.
  - verification: Execution Blueprint present and complete.
- Knowledge Compiler to Website Builder:
  - condition: Agent Package generated.
  - verification: package conforms to `standards/agent-package-standard.md`.
- Website Builder to Site Reviewer:
  - condition: static site deliverable created.
  - verification: required files exist and local inspection notes are present.
- Site Reviewer to Pipeline Supervisor:
  - condition: review report completed.
  - verification: requirements and contact placeholders reviewed.
- Pipeline Supervisor to Human Maintainer:
  - condition: supervisor report completed.
  - verification: final gate opened with context.

## Review Gates

- Static deliverable review:
  - owner: Site Reviewer.
  - criteria: two pages exist, navigation works, contact values are `da definire`, no realistic contact data appears, visual direction matches warm modern artisan target.
- Pipeline compliance review:
  - owner: Pipeline Supervisor.
  - criteria: required phases, gates, handoffs, review evidence and deliverables are present before final approval.

## Human Gates

- approve-execution-plan:
  - decision required: approve temporary agent team, workflow, handoffs, review gates and final gate before Agent Package generation and execution.
  - decision owner: Human Maintainer.
  - blocking scope: agent package generation and project execution.
- approve-final-delivery:
  - decision required: approve final completed work after Site Reviewer and Pipeline Supervisor reports.
  - decision owner: Human Maintainer.
  - blocking scope: project closure.

## Completion Criteria

- Static site exists under `projects/ceramirycs/deliverables/site/`.
- The site has exactly the requested public pages: landing and contact.
- Navigation between pages works.
- Contact page includes email, phone, address and Instagram, each as `da definire`.
- No realistic contact placeholder exists in deliverable files.
- Review report exists and has no blocking findings.
- Pipeline Supervisor report exists.
- `approve-final-delivery` is opened and decided by the human maintainer.

## Escalation Rules

- Stop if any required Human Gate is Pending and its blocking scope includes the next task.
- Stop if a realistic contact value is found in any deliverable file.
- Stop if implementation requires a backend, build tool, external service, real contact detail or deployment decision not approved in the blueprints.
- Return to Website Builder if Site Reviewer finds blocking issues.

## Parallelization Notes

No parallel execution is needed. The task is intentionally small and sequential handoffs keep validation clear.

## Runtime Preferences

Use the Codex Conversation Adapter for orchestration and the Codex Runtime Adapter semantics for each temporary Agent Package, while keeping execution in the same chat as requested.

## Knowledge Candidate Plan

Collect Knowledge Candidates only if the ad-hoc Website Builder role proves reusable or if standards lack checks for strict placeholder contact data. Do not integrate candidates automatically.
