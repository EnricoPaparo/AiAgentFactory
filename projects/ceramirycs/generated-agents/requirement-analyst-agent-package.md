# Agent Package: requirement-analyst-ceramirycs

## Metadata

- project-id: ceramirycs
- package-id: requirement-analyst-ceramirycs
- agent-role: Requirement Analyst
- agent-source: permanent agent `agents/requirement-analyst/requirement-analyst.md`
- runtime-adapter: runtime-adapters/codex-conversation.md

## Task

Transform the initial request into a verifiable Requirements Blueprint for the CeraMirycs website project.

## Inputs

- projects/ceramirycs/input/initial-request.md
- agents/requirement-analyst/requirement-analyst.md
- standards/requirements-blueprint-standard.md
- standards/handoff-standard.md

## Expected Outputs

- projects/ceramirycs/blueprints/requirements-blueprint.md
- projects/ceramirycs/handoffs/requirement-analyst-to-architect.md

## Boundaries

- Do not choose architecture or technology stack.
- Do not implement the website.
- Do not invent realistic contact data.
- Preserve open contact fields as empty or `da definire`.

## Workflow

1. Read the initial request.
2. Extract goal, output, requirements, constraints, assumptions, ambiguities and out-of-scope items.
3. Write acceptance criteria suitable for final review.
4. Produce handoff to Architect.
5. Stop at `approve-requirements`.

## Definition Of Done

- Requirements Blueprint follows `standards/requirements-blueprint-standard.md`.
- Functional requirements are verifiable.
- Contact placeholders are explicitly constrained.
- Handoff to Architect is present.
- No architecture or stack decision is made.
