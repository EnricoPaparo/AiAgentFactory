# Agent Package: requirement-analyst-agent-package

## Metadata

- package-id: requirement-analyst-agent-package
- project-id: ceramic-cozy-landing
- agent-role: Requirement Analyst
- agent-source:
  - type: permanent-agent
  - reference: agents/requirement-analyst/requirement-analyst.md
- assigned-capabilities:
  - capabilities/documentation.md

## Mission

Transform the user's website idea into a Requirements Blueprint for a minimal cozy ceramic website.

## Task

Read `projects/ceramic-cozy-landing/input/initial-request.md`, produce `projects/ceramic-cozy-landing/blueprints/requirements-blueprint.md`, and create a handoff to Architect.

## Inputs

- `projects/ceramic-cozy-landing/input/initial-request.md`
- `projects/ceramic-cozy-landing/blueprints/bootstrap-execution-blueprint.md`
- `projects/ceramic-cozy-landing/human-gates/approve-requirements.md`
- `agents/requirement-analyst/requirement-analyst.md`
- `standards/requirements-blueprint-standard.md`
- `standards/handoff-standard.md`
- `standards/human-gate-standard.md`
- `runtime-adapters/codex.md`
- `runtime-adapters/manual-execution.md`
- `capabilities/documentation.md`

## Expected Outputs

- `projects/ceramic-cozy-landing/blueprints/requirements-blueprint.md`
- `projects/ceramic-cozy-landing/handoffs/requirement-analyst-to-architect.md`

## Responsibilities

- Preserve the user's original intent.
- Define functional and non-functional requirements.
- Convert "cozy" and "modern" into explicit assumptions and acceptance criteria.
- Register ambiguities without blocking unnecessarily.
- Keep technical stack, architecture and implementation choices out of scope.
- Create a handoff to Architect.

## Boundaries

- Do not choose framework, tooling or file structure for the site.
- Do not implement the website.
- Do not generate Solution Blueprint or Execution Blueprint.
- Do not modify permanent standards, agents, archetypes, capabilities or runtime adapters.
- Do not decide the `approve-requirements` Human Gate.

## Tools

- Repository file reading and editing for project artifacts only.

## Workflow

1. Read Codex Adapter and Manual Execution Adapter.
2. Read the initial request.
3. Read Requirement Analyst definition and Requirements Blueprint Standard.
4. Check Human Gates. `approve-requirements` is `Pending` but blocks only `solution blueprint generation`, so it does not block this task.
5. Produce Requirements Blueprint.
6. Produce handoff to Architect.
7. If a reusable process improvement emerges, create a Knowledge Candidate.

## Handoff Requirements

Produce `projects/ceramic-cozy-landing/handoffs/requirement-analyst-to-architect.md` conforming to `standards/handoff-standard.md`.

## Definition of Done

- Requirements Blueprint exists.
- Requirements Blueprint contains all required sections from `standards/requirements-blueprint-standard.md`.
- Assumptions and ambiguities are separated.
- Acceptance criteria are verifiable.
- No stack or architecture is selected.
- Handoff to Architect exists.

## Runtime Hints

Use `runtime-adapters/codex.md`.

## Risk Notes

- The requested visual style is subjective, so assumptions must be explicit.
- Contact details must remain placeholders, not realistic fake personal data.

## Review Gates

- Human Maintainer should review requirements through `approve-requirements` before architecture work starts.

## Escalation Rules

- Block if the initial request file is missing.
- Block if a Human Gate `Pending` applies to this task.

## Knowledge Candidate Triggers

- Missing requirement fields for visual/design-heavy projects.
- Ambiguity about how to represent placeholder contact details.
