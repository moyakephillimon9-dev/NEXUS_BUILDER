# NEXUS Builder

An AI-powered software factory that orchestrates a team of specialised AI agents to plan, design, code, review, test, and deploy software projects from a single natural-language goal.

## Stack

- **Language**: Python 3
- **Architecture**: Plugin-based agent swarm
- **Storage**: In-memory shared state (`core/shared_memory.py`)

## How to Run

```
python nexus.py
```

You will be prompted:

```
Enter project goal :
```

Type any software goal (e.g. *Build a simple Calculator application*) and press Enter. The full pipeline runs automatically.

## Pipeline Sequence

```
Kernel Boot
    └─▶ [STAGE 0] Planner AI       — builds execution manifest
    └─▶ [STAGE 1] Architect AI     — designs system blueprint
    └─▶ [STAGE 2] Coder AI         — generates source code
    └─▶ [STAGE 3] Reviewer AI      — static analysis + quality gate
    └─▶ [STAGE 4] Tester AI        — runtime sandbox validation
    └─▶ [STAGE 5] Deployment AI    — packages and archives the release
```

## Output Artifacts

Each completed run produces a deployment folder under `deployments/<task_id>_<goal>/` containing:

| File               | Description                      |
|--------------------|----------------------------------|
| `main.py`          | Generated source code            |
| `requirements.txt` | Runtime dependencies             |
| `README.md`        | Auto-generated project readme    |
| `deployment.json`  | Release manifest with checksum   |

A full project archive is also saved to `projects/<task_id>.json`.

## Project Structure

```
nexus.py                  ← Entry point (prompt + pipeline launch)
core/
  kernel.py               ← System boot (plugin discovery, registry)
  orchestrator.py         ← Pipeline wiring and sequential dispatch
  config.py               ← Centralised paths and constants
  shared_memory.py        ← Key-value inter-agent state store
  ai_registry.py          ← Plugin registry
  plugin_manager.py       ← Auto-discovers plugin directories
  logger.py               ← Timestamped logger
plugins/
  manager_ai/             ← ManagerAI — swarm coordinator + strategic advisor
  planner_ai/             ← PlannerAI — execution manifest builder
  architect_ai/           ← ArchitectAI — system blueprint designer
  coder_ai/               ← CoderAI — goal-aware source code generator
  reviewer_ai/            ← ReviewerAI — static analysis + AST security scan
  tester_ai/              ← TesterAI — sandboxed runtime validation
  deployment_ai/          ← DeploymentAI — release packaging and archiving
test_enterprise_pipeline.py  ← Integration test (full enterprise pipeline)
test_nexus_pipeline.py       ← Lightweight pipeline smoke test
```

## User Preferences

- Preserve all existing plugin agents and enterprise features — do not remove functionality.
- Pipeline order: Planner AI → Architect AI → Coder AI → Reviewer AI → Tester AI → Deployment AI.
- CoderAI is goal-aware: detects keywords (e.g. "calculator") and generates matching code.
