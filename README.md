# AiAgentFactory

A structured knowledge repository for designing, generating, orchestrating, supervising, and evolving temporary teams of specialized AI agents for software development projects.

AiAgentFactory is **not** a runtime, framework, or prompt library. It is the architectural reference of the factory: it defines identities, boundaries, components, workflows, contracts, and invariant rules. Operational standards for individual artifacts live in `standards/`.

---

## Why This Exists

Large software projects run by AI agents fail in predictable ways: overlapping responsibilities, missing handoffs, no human checkpoints, and zero knowledge retention between runs. AiAgentFactory solves this by treating agent-based development as a **factory process** — with permanent governance roles, formal contracts between agents, mandatory human decision gates, and a controlled knowledge evolution cycle.

---

## How It Works

```text
User Request
  → Requirement Analyst       (clarifies requirements)
  → Requirements Blueprint
  → Architect                 (designs the solution)
  → Solution Blueprint
  → Pipeline Designer         (designs the workflow)
  → Execution Blueprint
  → Knowledge Compiler        (assembles agent packages)
  → Agent Package(s)
  → Runtime Adapter           (translates to a specific runtime)
  → Project Team Execution
  → Pipeline Supervisor       (verifies process compliance)
  → Knowledge Evolution       (reviews improvement proposals)
  → controlled update of permanent knowledge
```

Each step produces a versioned artifact with an explicit owner, inputs, outputs, and a Definition of Done. Nothing advances without a verified handoff. Human decisions are enforced through blocking Human Gates.

---

## Repository Structure

```text
AiAgentFactory/
├── AgentFactory.md              # Full architectural reference (start here)
├── implementation-status.md     # Current implementation progress
│
├── agents/                      # Permanent factory agents (governance roles)
│   ├── requirement-analyst/
│   ├── architect/
│   ├── pipeline-designer/
│   ├── pipeline-supervisor/
│   ├── knowledge-compiler/
│   └── knowledge-evolution/
│
├── archetypes/                  # Reusable templates for temporary agents
│   ├── developer.md
│   ├── tester.md
│   ├── reviewer.md
│   ├── security-auditor.md
│   └── documentation-writer.md
│
├── capabilities/                # Reusable operational knowledge packages
│   ├── git-workflow.md
│   ├── code-review.md
│   ├── testing-strategy.md
│   ├── node.md
│   ├── react.md
│   ├── api-security.md
│   └── documentation.md
│
├── standards/                   # Format contracts for all artifacts
│   ├── agent-package-standard.md
│   ├── handoff-standard.md
│   ├── human-gate-standard.md
│   ├── execution-blueprint-standard.md
│   ├── requirements-blueprint-standard.md
│   ├── solution-blueprint-standard.md
│   ├── capability-standard.md
│   └── knowledge-candidate-standard.md
│
├── runtime-adapters/            # Translation rules per runtime
│   ├── manual-execution.md
│   └── codex.md
│
└── projects/                    # Project workspaces (temporary, per-project)
    └── _template/               # Copy this to start a new project
```

**Where to put what:**

| Knowledge type | Destination |
|---|---|
| Permanent agent behavior rule | `agents/<agent-name>/` |
| Reusable temporary agent template | `archetypes/<role>.md` |
| Reusable technical knowledge | `capabilities/<topic>.md` |
| Artifact format contract | `standards/<artifact>-standard.md` |
| Runtime translation rules | `runtime-adapters/<runtime>.md` |
| Project-specific work | `projects/<project-id>/` |
| Improvement proposal (not yet approved) | `projects/<project-id>/knowledge-candidates/` |

---

## Quickstart: Start a New Project

**Prerequisites:** The factory has at least MVP 1-3 complete (standards, permanent agents, archetypes). See `implementation-status.md`.

**Step 1 — Create the project workspace**

```bash
cp -r projects/_template projects/<your-project-id>
```

**Step 2 — Write the initial request**

Create `projects/<your-project-id>/input/initial-request.md` with:
- What the user or stakeholder wants
- Known constraints and deadlines
- Any relevant context or existing artifacts

**Step 3 — Run the factory flow**

Activate each permanent agent in sequence using the appropriate runtime adapter:

1. `agents/requirement-analyst/` → produces `blueprints/requirements-blueprint.md`
2. `agents/architect/` → produces `blueprints/solution-blueprint.md`
3. `agents/pipeline-designer/` → produces `blueprints/execution-blueprint.md`
4. `agents/knowledge-compiler/` → produces `generated-agents/` packages
5. Execute agents via `runtime-adapters/` of your choice
6. `agents/pipeline-supervisor/` → verifies process compliance
7. `agents/knowledge-evolution/` → evaluates any Knowledge Candidates produced

**Step 4 — Respect Human Gates**

Any `human-gates/` file with status `Pending` **blocks** all tasks in its `blocking-scope`. Do not advance the workflow until a human decision is recorded.

**Step 5 — Collect Knowledge Candidates**

At the end of the project, review `knowledge-candidates/`. Approved candidates become permanent knowledge through the Knowledge Evolution agent.

See `projects/_template/README.md` for the complete folder guide.

---

## Key Documents

| Document | Purpose |
|---|---|
| `AgentFactory.md` | Full architectural reference — invariants, concepts, workflows |
| `standards/agent-package-standard.md` | How to build a valid Agent Package |
| `standards/handoff-standard.md` | Required fields for agent-to-agent delivery |
| `standards/human-gate-standard.md` | How to define and enforce Human Gates |
| `runtime-adapters/manual-execution.md` | How to run the factory without an orchestrator |
| `runtime-adapters/codex.md` | How to run Agent Packages in Codex |
| `CONTRIBUTING.md` | How to extend the factory (capabilities, archetypes, standards) |
| `GLOSSARY.md` | Definitions of all factory terms |

---

## Current Status

See `implementation-status.md` for the detailed progress tracker.

**MVP summary:**
- MVP 1 (Standards): Complete — all 8 format contracts defined
- MVP 2 (Permanent Agents): Complete — all 6 permanent agents defined
- MVP 3 (Archetypes): Complete — 5 base archetypes defined
- MVP 4 (First Execution): Complete — pilot project executed end-to-end

---

## Language Policy

All documentation in this repository is written in **Italian**. New files and contributions should follow the same language. See `CONTRIBUTING.md` for contribution guidelines.

---

## Invariant Rules

These rules hold regardless of runtime, AI model, or tooling changes:

1. Permanent knowledge is the factory's primary asset.
2. Temporary agents are disposable — created per project, not permanent.
3. No proposal generated during a project automatically updates permanent knowledge.
4. Runtimes are interchangeable and must not contain factory decision logic.
5. Roles, responsibilities, contracts, and workflows are defined before technical execution.
6. Every significant step has explicit input, output, owner, and completion criteria.
7. The Project Workspace contains temporary work, not approved knowledge.
8. The Pipeline Supervisor validates process compliance — it is not an omniscient super-agent.
9. A Pending Human Gate blocks all tasks in its declared blocking scope.
10. Code is an operational tool, not the center of the factory.
