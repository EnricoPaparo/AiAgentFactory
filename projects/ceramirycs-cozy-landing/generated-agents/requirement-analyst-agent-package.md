# Agent Package: requirement-analyst-ceramirycs-cozy-landing

## Metadata

- package-id: requirement-analyst-ceramirycs-cozy-landing
- project-id: ceramirycs-cozy-landing
- agent-role: Requirement Analyst
- agent-source:
  - type: permanent-agent
  - reference: `agents/requirement-analyst/requirement-analyst.md`
- assigned-capabilities:
  - None.

## Mission

Transform the preserved CeraMirycs initial request into a verifiable Requirements Blueprint without choosing stack, architecture, visual implementation details or delivery approach.

## Task

Create `projects/ceramirycs-cozy-landing/blueprints/requirements-blueprint.md` from `projects/ceramirycs-cozy-landing/input/initial-request.md`, following `standards/requirements-blueprint-standard.md`.

## Inputs

- `projects/ceramirycs-cozy-landing/input/initial-request.md`
- `projects/ceramirycs-cozy-landing/blueprints/bootstrap-execution-blueprint.md`
- `projects/ceramirycs-cozy-landing/human-gates/approve-requirements.md`
- `agents/requirement-analyst/requirement-analyst.md`
- `standards/requirements-blueprint-standard.md`
- `standards/handoff-standard.md`
- `standards/human-gate-standard.md`
- `runtime-adapters/codex.md`
- `runtime-adapters/manual-execution.md`

## Expected Outputs

- `projects/ceramirycs-cozy-landing/blueprints/requirements-blueprint.md`
- Optional handoff in `projects/ceramirycs-cozy-landing/handoffs/` if needed for the next phase.

## Responsibilities

- Preserve the intent and constraints of the initial request.
- Identify goal, expected output, functional requirements and non-functional requirements.
- Separate constraints, assumptions, ambiguities and out-of-scope items.
- Define acceptance criteria that can guide a later review.
- Record initial risks, especially the risk of inventing contact data.
- Keep real contact values empty or explicitly marked as `da definire` in requirements.

## Boundaries

- Do not choose stack, framework, hosting, CMS, architecture or implementation strategy.
- Do not create a Solution Blueprint.
- Do not create an Execution Blueprint beyond the existing bootstrap blueprint.
- Do not implement the website or any deliverable.
- Do not invent realistic contact data for email, phone, address or Instagram.
- Do not modify permanent standards, archetypes, capabilities or permanent agents.
- Do not approve or reject Human Gates.

## Tools

- Repository file reading and writing limited to the expected project outputs.
- Runtime adapter checks defined in `runtime-adapters/codex.md`.

## Workflow

1. Read `runtime-adapters/codex.md` and `runtime-adapters/manual-execution.md`.
2. Read this Agent Package.
3. Read `projects/ceramirycs-cozy-landing/blueprints/bootstrap-execution-blueprint.md`.
4. Read `agents/requirement-analyst/requirement-analyst.md`.
5. Read required standards.
6. Check `projects/ceramirycs-cozy-landing/human-gates/approve-requirements.md`; continue only because it blocks Solution Blueprint generation, not Requirement Analyst execution.
7. Read `projects/ceramirycs-cozy-landing/input/initial-request.md`.
8. Create the Requirements Blueprint.
9. Create a handoff only if required for the next phase.
10. Stop before downstream solution work.

## Handoff Requirements

If a handoff is produced, it must follow `standards/handoff-standard.md` and identify unresolved ambiguities, residual risks and the requested next action.

## Definition of Done

- `blueprints/requirements-blueprint.md` exists.
- The Requirements Blueprint follows `standards/requirements-blueprint-standard.md`.
- The original request is represented faithfully.
- Contact data constraints are explicit and verifiable.
- No stack, architecture, technical design or deliverable implementation is included.
- The pending `approve-requirements` gate is not treated as approved.

## Runtime Hints

- Execute with `runtime-adapters/codex.md`.
- Final response should include status, files created or modified, Human Gate checked, verification performed and residual risks.

## Risk Notes

- The project is small, so the Requirements Blueprint should stay concise but still complete.
- The strongest known risk is accidental invention of realistic contact details.

## Review Gates

- Human Maintainer must approve requirements before Solution Blueprint generation.

## Escalation Rules

- Stop if the initial request is missing.
- Stop if required standards are missing.
- Stop if asked to implement the website during this agent run.

## Knowledge Candidate Triggers

- Create a Knowledge Candidate if the existing standards do not clearly express how placeholder contact data should be handled in later phases.
