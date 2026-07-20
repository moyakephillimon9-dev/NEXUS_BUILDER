---
name: Pipeline architecture
description: 21-stage NEXUS pipeline v3 — all 22 worker IDs, stage order, MemoryAI asyncio fix
---

## Worker IDs and stage order (v3.0.0)
VISION-001 (0), ASSESS-001 (1), RESEARCH-001 (2), MODULE-001 (3),
PLANNER-001 (4), ARCHITECT-001 (5), DATABASE-001 (6), CODER-001 (7),
DESIGN-001 (8), REVIEWER-001 (9), TESTER-001 (10), SECURITY-001 (11),
PERFORMANCE-001 (12), DOCS-001 (13), MONITOR-001 (14), INTEGRATION-001 (15),
DEVOPS-001 (16), DEPLOY-001 (17), VERIFY-001 (18), PROGRESS-001 (19), MEMORY-001 (20).

Total: 22 agents (Manager + 21 workers), 21 stages.

## MemoryAI asyncio deadlock fix
`learn_project()` + `_atomic_save()` both acquired `self._lock` (asyncio.Lock is not reentrant).
Fix: `process_project_task()` (sync pipeline entry) + `_sync_save()` (no lock) added.

**Why:** asyncio.Lock is not reentrant; calling it twice in the same coroutine deadlocks.
**How to apply:** Any new worker that wraps async methods must not re-acquire a held lock.

## Shared Memory keys
- Active project: `f"active_project_{task_id}"`
- Research context: `f"research_context_{task_id}"`

## Knowledge stores
- `research/knowledge_base.json` — Research AI topic store (SHA-256 dedup)
- `memory/database.json` — Memory AI knowledge graph
