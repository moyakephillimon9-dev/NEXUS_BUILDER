# NEXUS Builder

An AI-powered software factory that orchestrates a team of 22 specialised AI agents across a 21-stage pipeline to plan, design, code, review, test, secure, document, and deploy software projects from a single natural-language goal or vision document.

**Owner:** Moyake Phillimon  
**Version:** 0.0.4  
**Language:** Python 3.12 (stdlib only — no external dependencies required)

---

## How to Run

### Interactive menu (default)

```bash
python nexus.py
```

Choose from the menu:
- `[1]` Run pipeline with a typed goal
- `[2]` Run pipeline from a vision document file
- `[3]` List all 22 AI workers
- `[4]` View project history
- `[5]` About NEXUS Builder

### One-shot goal

```bash
python nexus.py --goal "Build a REST API"
```

### Vision document

```bash
python nexus.py --vision path/to/vision.txt
python nexus.py --vision -          # read from stdin
```

### Other flags

```bash
python nexus.py --workers           # list all AI workers
python nexus.py --history           # show completed project history
python nexus.py --version           # print version
```

---

## Pipeline (21 stages, 22 agents)

| Stage | Worker ID       | Agent                  | Role |
|------:|-----------------|------------------------|------|
|     0 | VISION-001      | Vision Parser AI       | Parses vision docs; extracts requirements, modules, technologies |
|     1 | ASSESS-001      | Capability Assessor    | Classifies features: Fully/Partially/Unsupported |
|     2 | RESEARCH-001    | Research AI            | Permanent knowledge base; pattern library |
|     3 | MODULE-001      | Module Detector AI     | Detects modules, builds dependency graph |
|     4 | PLANNER-001     | Planner AI             | 19-phase plan with tasks, effort, risk, calendar |
|     5 | ARCHITECT-001   | Architect AI           | 9-layer architecture design |
|     6 | DATABASE-001    | Database AI            | SQL DDL schema + Python sqlite3 helper |
|     7 | CODER-001       | Coder AI               | 13-template type-aware source code generation |
|     8 | DESIGN-001      | Design AI              | Colour palette, production CSS, layout spec |
|     9 | REVIEWER-001    | Reviewer AI            | AST static analysis + quality gate (score ≥ 70) |
|    10 | TESTER-001      | Tester AI              | Sandboxed runtime validation + coverage estimation |
|    11 | SECURITY-001    | Security AI            | Vulnerability & secret scanning; risk classification |
|    12 | PERFORMANCE-001 | Performance AI         | Benchmarks + cyclomatic complexity; grade A–F |
|    13 | DOCS-001        | Documentation AI       | README, API.md, ARCHITECTURE.md, CHANGELOG, CONTRIBUTING |
|    14 | MONITOR-001     | Monitoring AI          | Health checks, metrics, logger config, alerts.json |
|    15 | INTEGRATION-001 | Integration AI         | API client with retries, HMAC webhook handler |
|    16 | DEVOPS-001      | DevOps AI              | Dockerfile, GitHub Actions CI/CD, Makefile |
|    17 | DEPLOY-001      | Deployment AI          | Release archive, requirements.txt, deployment.json |
|    18 | VERIFY-001      | Verification AI        | Pre-release honesty check — blocks false success claims |
|    19 | PROGRESS-001    | Progress Tracker AI    | Completion %, feature classification, limitations |
|    20 | MEMORY-001      | Memory AI              | Persistent semantic knowledge graph + learning engine |

---

## Output Artifacts

Each completed run produces a deployment folder under `deployments/<task_id>_<goal>/`:

| File               | Description                              |
|--------------------|------------------------------------------|
| `main.py`          | Generated source code                    |
| `requirements.txt` | Runtime dependencies for generated app   |
| `README.md`        | Auto-generated project readme            |
| `deployment.json`  | Release manifest with checksum           |
| `schema.sql`       | Database schema                          |
| `Dockerfile`       | Container definition                     |
| `Makefile`         | Build/run commands                       |
| `docs/`            | Full documentation suite (5 files)       |

A full project record is also saved to `projects/<task_id>.json`.

---

## Project Structure

```
nexus.py                      ← CLI entry point
core/
  kernel.py                   ← System boot (plugin discovery, registry)
  orchestrator.py             ← 21-stage pipeline wiring and dispatch
  config.py                   ← Centralised paths and constants
  shared_memory.py            ← Key-value inter-agent state store
  ai_registry.py              ← Plugin registry
  plugin_manager.py           ← Auto-discovers plugin directories
  logger.py                   ← Timestamped logger
plugins/                      ← 22 AI agent plugins (one folder each)
memory/                       ← Persistent knowledge graph (database.json)
logs/                         ← Runtime logs (auto-created)
tests/                        ← Test directory
deployments/                  ← Generated project output (git-ignored)
projects/                     ← Completed project records (git-ignored)
```

---

## Core Principle

> **Honesty, verification, and transparency take priority over claiming completion.**

NEXUS never fakes unsupported features. The Verification AI (stage 18) blocks any pipeline run from reporting success if the claimed capabilities don't match what was actually built.

---

## User Preferences

- Preserve all existing plugin agents and enterprise features — do not remove functionality.
- Pipeline order: Vision → Assess → Research → Module → Planner → Architect → Database → Coder → Design → Reviewer → Tester → Security → Performance → Docs → Monitor → Integration → DevOps → Deploy → Verify → Progress → Memory.
- CoderAI is goal-aware: detects keywords (e.g. "calculator", "api", "web") and generates matching templates.
- No external dependencies — keep the project stdlib-only unless an LLM integration is explicitly added.
