---
name: Pipeline architecture
description: 16-stage NEXUS pipeline — worker IDs, stage order, MemoryAI asyncio fix
---

## Worker IDs and stage order
RESEARCH-001 (Stage 0), PLANNER-001 (1), ARCHITECT-001 (2), DATABASE-001 (3),
CODER-001 (4), DESIGN-001 (5), REVIEWER-001 (6), TESTER-001 (7),
SECURITY-001 (8), PERFORMANCE-001 (9), DOCS-001 (10), MONITOR-001 (11),
INTEGRATION-001 (12), DEVOPS-001 (13), DEPLOY-001 (14), MEMORY-001 (15).

## MemoryAI asyncio deadlock fix
`learn_project()` + `_atomic_save()` both acquired `self._lock` (asyncio.Lock is not reentrant).
Fix: `process_project_task()` (sync pipeline entry) + `_sync_save()` (no lock) added.

**Why:** asyncio.Lock is not reentrant; calling it twice in the same coroutine deadlocks.
**How to apply:** Any new worker that wraps async methods must not re-acquire a held lock.

## Shared Memory keys
- Active project: `f"active_project_{task_id}"`
- Research context: `f"research_context_{task_id}"`

## Research AI knowledge stores
- `research/knowledge_base.json` — topic store (SHA-256 dedup)
- `memory/database.json` — Memory AI knowledge graph
