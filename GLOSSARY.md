# Glossary

Precise definitions of all terms used in AiAgentFactory. When a term appears in any factory document, it has exactly the meaning defined here.

---

## Agent Package

A self-contained operational specification that describes a temporary agent ready to be executed by a runtime adapter. An Agent Package is runtime-agnostic — it does not depend on any specific execution environment.

An Agent Package is composed by the **Knowledge Compiler** from:
- a role source (existing archetype or ad-hoc definition in the Execution Blueprint)
- relevant capabilities
- project context
- assigned task
- available tools
- operational rules
- completion criteria

Format defined in: `standards/agent-package-standard.md`

---

## Archetype

A reusable, approved skeleton for generating temporary agents of a recurring type. An archetype defines role, responsibilities, inputs, outputs, boundaries, and Definition of Done. It does **not** contain technology-specific knowledge (that belongs in capabilities). Archetypes are a starting point, not a constraint — the Pipeline Designer can define ad-hoc agents when no existing archetype fits.

Stored in: `archetypes/`

---

## Capability

A package of reusable operational knowledge for a specific technology, domain, or practice. Capabilities contain best practices, checklists, failure modes, risks, and review criteria. They are **not** tutorials or introductions — they are operational references that agents use while executing a task.

Capabilities are assigned to temporary agents in the Agent Package. Multiple capabilities can be combined.

Examples: `node.md`, `api-security.md`, `git-workflow.md`

Format defined in: `standards/capability-standard.md`  
Stored in: `capabilities/`

---

## Definition of Done (DoD)

A set of verifiable conditions that determine when a task or artifact is complete. Every permanent agent, archetype, and Agent Package must define a Definition of Done. The Pipeline Supervisor uses the DoD to verify task completion without substituting for the technical agent.

---

## Execution Blueprint

The operational plan for a project. It defines the agent team (roles, sources, capabilities), the workflow (sequence, parallelism), handoff assignments, review gates, Human Gates, and completion criteria. The Execution Blueprint is produced by the **Pipeline Designer** and consumed by the **Knowledge Compiler** and **Pipeline Supervisor**.

Format defined in: `standards/execution-blueprint-standard.md`

---

## Handoff

A formal delivery contract between agents or phases. A handoff is not a narrative summary — it is a verifiable transfer of responsibility. Every handoff must declare: what was completed, what was produced, which files were touched, which decisions were made, what problems remain open, residual risks, the requested next action, and criteria to verify the output.

A missing or vague handoff is a factory failure mode.

Format defined in: `standards/handoff-standard.md`

---

## Human Gate

A mandatory decision point where the factory must stop and wait for a human decision before proceeding. Human Gates are defined by the **Pipeline Designer** and enforced by the **Pipeline Supervisor** and runtime adapters.

**Key invariant:** When a Human Gate is `Pending`, **no task in its declared `blocking-scope` may execute**. There are no exceptions.

Human Gate statuses: `Pending` → `Approved` / `Rejected` / `Changes Requested` / `Expired` / `Cancelled`

Format defined in: `standards/human-gate-standard.md`

---

## Knowledge Candidate

A structured improvement proposal generated during a project. Any agent or phase can produce a Knowledge Candidate when it identifies a reusable lesson, a new best practice, a failure mode, or a gap in existing knowledge.

Knowledge Candidates are temporary artifacts — they live in the project workspace. They become permanent knowledge **only** after evaluation and approval by the **Knowledge Evolution** agent.

Statuses: `Proposed` → `Reviewed` → `Accepted` → `Integrated`  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;`→ Rejected`

Format defined in: `standards/knowledge-candidate-standard.md`

---

## Knowledge Compiler

The permanent agent responsible for composing Agent Packages. The Knowledge Compiler takes an Execution Blueprint, selects or receives archetypes or ad-hoc definitions, assigns relevant capabilities, and assembles complete, executable Agent Packages. It does not make project strategy decisions and does not supervise execution.

Defined in: `agents/knowledge-compiler/`

---

## Knowledge Evolution

The permanent agent responsible for evaluating Knowledge Candidates and deciding whether they become permanent knowledge. Knowledge Evolution distinguishes between locally useful knowledge (stays in the project) and genuinely reusable knowledge (promotes to permanent files). It never integrates a proposal automatically.

Defined in: `agents/knowledge-evolution/`

---

## Permanent Agent

A stable governance role in the factory. Permanent agents define and govern the factory's core process — they do not do project implementation work. The six permanent agents are: Requirement Analyst, Architect, Pipeline Designer, Knowledge Compiler, Pipeline Supervisor, and Knowledge Evolution.

Permanent agents have a single, clearly bounded responsibility. They do not overlap.

Stored in: `agents/`

---

## Pipeline Designer

The permanent agent that transforms Requirements Blueprint and Solution Blueprint into an Execution Blueprint. The Pipeline Designer designs the agent team, the workflow, handoffs, review gates, and Human Gates. It does not execute the project and does not modify permanent knowledge.

Defined in: `agents/pipeline-designer/`

---

## Pipeline Supervisor

The permanent agent that verifies process compliance during and after project execution. The Pipeline Supervisor checks that handoffs are present and complete, review gates were executed, Human Gates were respected, and completion criteria are met. It does **not** substitute for technical agents (Developer, Tester, Reviewer, etc.) — it validates process, not technical correctness.

Defined in: `agents/pipeline-supervisor/`

---

## Project Workspace

The temporary working directory for a specific project. It contains all project-specific artifacts: input, blueprints, generated Agent Packages, handoffs, Human Gates, deliverables, reviews, and Knowledge Candidates. Project Workspaces contain **temporary knowledge only** — approved permanent knowledge changes go through Knowledge Evolution.

Template: `projects/_template/`  
Stored in: `projects/<project-id>/`

---

## Requirements Blueprint

The structured artifact produced by the Requirement Analyst from a user request. It contains: objective, functional and non-functional requirements, constraints, assumptions, ambiguities, out-of-scope items, acceptance criteria, and initial risks. It does **not** contain architectural decisions or stack choices.

Format defined in: `standards/requirements-blueprint-standard.md`

---

## Review Gate

A mandatory checkpoint where a technical agent (Reviewer, Tester, Security Auditor, etc.) verifies a specific output before the workflow can advance. Review Gates are declared in the Execution Blueprint and enforced by the Pipeline Supervisor. A Review Gate that was declared but not executed is a factory failure mode.

---

## Runtime Adapter

A set of translation rules that convert a generic Agent Package into the format and execution model required by a specific runtime (e.g., Codex, manual execution, OpenAI Agents SDK, LangGraph). Runtime Adapters translate — they do not contain factory decision logic. The factory's core logic (roles, standards, handoffs, gates) remains the same regardless of which runtime adapter is used.

Stored in: `runtime-adapters/`

---

## Solution Blueprint

The technical design artifact produced by the Architect from a Requirements Blueprint. It contains: proposed architecture, tech stack, components, data flows, integrations, security strategy, trade-offs, rejected alternatives, technical risks, and implementation strategy. The Architect does not build the agent team — that is the Pipeline Designer's job.

Format defined in: `standards/solution-blueprint-standard.md`

---

## Subagent (Temporary Agent)

An agent created for a specific project or task. Subagents are disposable — they can be archived or destroyed when the project ends. They are composed by the Knowledge Compiler from an archetype or ad-hoc definition plus relevant capabilities and project context.

Subagents are distinct from Permanent Agents: they do project work, not factory governance.

---

## Temporary vs Permanent Knowledge

| | Temporary Knowledge | Permanent Knowledge |
|---|---|---|
| **Lives in** | `projects/<project-id>/` | `agents/`, `archetypes/`, `capabilities/`, `standards/`, `runtime-adapters/` |
| **Scope** | One project or task | All future projects |
| **Created by** | Any agent during execution | Knowledge Evolution (after approval) |
| **Survives project end** | Archived, not promoted | Yes |
| **Entry gate** | None | Knowledge Candidate → Knowledge Evolution |
