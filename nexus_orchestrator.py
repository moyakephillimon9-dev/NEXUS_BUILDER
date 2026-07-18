"""
NEXUS Core
Orchestrator AI — Dynamic DAG Parallel Topology Engine

Module ID : NEXUS-ORCHESTRATOR-DAG
Version   : 5.0.0
"""

import asyncio
import json
import logging
import time

from pathlib import Path
from enum import Enum
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any, Protocol

try:
    import psutil
except ImportError:
    psutil = None

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except Exception:
    pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s : %(message)s"
)

logger = logging.getLogger("NEXUS")


class StepStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    ROLLED_BACK = "ROLLED_BACK"


class SharedMemoryProtocol(Protocol):

    def read(self, key: str) -> Optional[Dict[str, Any]]:
        ...

    def write(self, key: str, value: Dict[str, Any]) -> None:
        ...


class WorkerProtocol(Protocol):

    async def execute(
        self,
        task_id: str,
        context: Dict[str, Any]
    ) -> bool:
        ...

    async def rollback(
        self,
        task_id: str,
        context: Dict[str, Any]
    ) -> None:
        ...

    async def health_check(self) -> bool:
        ...


@dataclass(slots=True)
class WorkerMetrics:

    runtime: float = 0.0
    retries: int = 0
    cpu_percent: float = 0.0
    memory_mb: float = 0.0


@dataclass(slots=True)
class PipelineStep:

    id: str

    dependencies: List[str] = field(default_factory=list)

    status: StepStatus = StepStatus.PENDING

    started: Optional[str] = None

    ended: Optional[str] = None

    error: Optional[str] = None

    metrics: WorkerMetrics = field(default_factory=WorkerMetrics)


@dataclass(slots=True)
class ExecutionContext:

    task_id: str

    project: Dict[str, Any]

    steps: Dict[str, PipelineStep] = field(default_factory=dict)

    metadata: Dict[str, Any] = field(default_factory=dict)

    cancel_event: asyncio.Event = field(default_factory=asyncio.Event)


class OrchestratorAI:

    def __init__(
        self,
        memory: SharedMemoryProtocol,
        config: Optional[str] = None,
        timeout: float = 300.0,
    ):

        self.memory = memory

        self.timeout = timeout

        self.workers: Dict[str, WorkerProtocol] = {}

        self.pipeline: List[Dict[str, Any]] = []

        self.active: Dict[str, ExecutionContext] = {}

        self._load_pipeline(config)

    def _load_pipeline(self, config: Optional[str]) -> None:
        """
        Load pipeline configuration from disk.
        Falls back to the default production topology.
        """

        if config and Path(config).exists():
            try:
                with open(config, "r", encoding="utf-8") as fp:
                    self.pipeline = json.load(fp)

                logger.info("Loaded external pipeline configuration.")
                self._validate_pipeline()
                return

            except Exception as exc:
                logger.error(
                    f"Unable to load pipeline configuration: {exc}"
                )

        self.pipeline = [
            {
                "id": "PLANNER-001",
                "dependencies": [],
                "timeout": 30.0,
            },
            {
                "id": "ARCHITECT-001",
                "dependencies": ["PLANNER-001"],
                "timeout": 45.0,
            },
            {
                "id": "CODER-001",
                "dependencies": ["ARCHITECT-001"],
                "timeout": 120.0,
            },
            {
                "id": "AUDITOR-001",
                "dependencies": ["ARCHITECT-001"],
                "timeout": 60.0,
            },
            {
                "id": "TESTER-001",
                "dependencies": [
                    "CODER-001",
                    "AUDITOR-001",
                ],
                "timeout": 90.0,
            },
            {
                "id": "DEPLOY-001",
                "dependencies": ["TESTER-001"],
                "timeout": 60.0,
            },
        ]

        logger.info("Loaded default production topology.")
        self._validate_pipeline()

    def _validate_pipeline(self) -> None:
        """
        Detect dependency cycles using Kahn's Algorithm.
        """

        graph = {}
        indegree = {}

        for item in self.pipeline:
            sid = item["id"]
            graph[sid] = []
            indegree[sid] = 0

        for item in self.pipeline:
            sid = item["id"]

            for dep in item["dependencies"]:
                graph[dep].append(sid)
                indegree[sid] += 1

        queue = [
            node
            for node, degree in indegree.items()
            if degree == 0
        ]

        visited = 0

        while queue:

            node = queue.pop(0)

            visited += 1

            for nxt in graph[node]:

                indegree[nxt] -= 1

                if indegree[nxt] == 0:
                    queue.append(nxt)

        if visited != len(self.pipeline):
            raise RuntimeError(
                "Pipeline contains cyclic dependencies."
            )

    def register_worker(
        self,
        worker_id: str,
        worker: WorkerProtocol,
    ) -> None:

        self.workers[worker_id] = worker

        logger.info(
            f"Registered worker: {worker_id}"
        )

    async def verify_cluster_health(self) -> bool:

        failed = []

        for wid, worker in self.workers.items():

            try:

                healthy = await worker.health_check()

                if not healthy:
                    failed.append(wid)

            except Exception:

                failed.append(wid)

        if failed:

            logger.error(
                f"Cluster health failed: {failed}"
            )

            return False

        logger.info("Cluster health OK.")

        return True

    def cancel_pipeline(
        self,
        task_id: str,
    ) -> bool:

        ctx = self.active.get(task_id)

        if ctx is None:
            return False

        ctx.cancel_event.set()

        logger.warning(
            f"Cancellation requested for {task_id}"
        )

        return True

    async def execute_pipeline(
        self,
        task_id: str,
    ) -> bool:

        if not await self.verify_cluster_health():
            return False

        project_key = f"active_project_{task_id}"

        loop = asyncio.get_running_loop()

        project = await loop.run_in_executor(
            None,
            self.memory.read,
            project_key,
        )

        if project is None:
            logger.error(
                f"Project '{project_key}' not found."
            )
            return False

        ctx = ExecutionContext(
            task_id=task_id,
            project=project,
            steps={
                item["id"]: PipelineStep(
                    id=item["id"],
                    dependencies=item["dependencies"],
                )
                for item in self.pipeline
            },
        )

        self.active[task_id] = ctx

        completed_events = {
            sid: asyncio.Event()
            for sid in ctx.steps
        }

        failure_event = asyncio.Event()

        executed_steps = []

        execution_lock = asyncio.Lock()

        async def run_step(
            item: Dict[str, Any],
        ) -> bool:

            step_id = item["id"]

            timeout = item.get(
                "timeout",
                60.0,
            )

            step = ctx.steps[step_id]

            try:

                if step.dependencies:

                    await asyncio.gather(
                        *(
                            completed_events[d].wait()
                            for d in step.dependencies
                        )
                    )

                if (
                    ctx.cancel_event.is_set()
                    or failure_event.is_set()
                ):

                    step.status = StepStatus.SKIPPED

                    completed_events[step_id].set()

                    return False

                worker = self.workers.get(step_id)

                if worker is None:

                    step.status = StepStatus.FAILED

                    step.error = (
                        "Worker not registered."
                    )

                    failure_event.set()

                    completed_events[step_id].set()

                    return False

                step.status = StepStatus.RUNNING

                step.started = (
                    datetime.now(
                        timezone.utc
                    ).isoformat()
                )

                start = time.perf_counter()

                cpu_before = (
                    psutil.Process().cpu_percent()
                    if psutil
                    else 0.0
                )

                success = await asyncio.wait_for(
                    worker.execute(
                        task_id,
                        ctx.project,
                    ),
                    timeout=timeout,
                )

                step.metrics.runtime = (
                    time.perf_counter()
                    - start
                )

                if psutil:
                    process = psutil.Process()

                    step.metrics.cpu_percent = (
                        process.cpu_percent()
                        - cpu_before
                    )

                    step.metrics.memory_mb = (
                        process.memory_info().rss
                        / 1024
                        / 1024
                    )

                step.ended = (
                    datetime.now(
                        timezone.utc
                    ).isoformat()
                )

                if success:

                    step.status = (
                        StepStatus.COMPLETED
                    )

                    async with execution_lock:
                        executed_steps.append(
                            step_id
                        )

                else:

                    step.status = (
                        StepStatus.FAILED
                    )

                    failure_event.set()

                completed_events[
                    step_id
                ].set()

                return success

            except Exception as exc:

                step.status = StepStatus.FAILED

                step.error = str(exc)

                step.ended = (
                    datetime.now(
                        timezone.utc
                    ).isoformat()
                )

                failure_event.set()

                completed_events[
                    step_id
                ].set()

                return False

        try:

            tasks = [
                asyncio.create_task(
                    run_step(item)
                )
                for item in self.pipeline
            ]

            results = await asyncio.wait_for(
                asyncio.gather(
                    *tasks,
                    return_exceptions=True,
                ),
                timeout=self.timeout,
            )

            success = (
                all(r is True for r in results)
                and not failure_event.is_set()
                and not ctx.cancel_event.is_set()
            )

            if success:

                logger.info(
                    f"Pipeline [{task_id}] completed successfully."
                )

                self.memory.write(
                    f"pipeline_result_{task_id}",
                    {
                        "status": "COMPLETED",
                        "timestamp": datetime.now(
                            timezone.utc
                        ).isoformat(),
                        "steps": {
                            sid: asdict(step)
                            for sid, step in ctx.steps.items()
                        },
                    },
                )

                return True

            logger.error(
                f"Pipeline [{task_id}] failed. Beginning rollback."
            )

            await self.rollback_pipeline(
                ctx,
                executed_steps,
            )

            return False

        except asyncio.TimeoutError:

            logger.error(
                f"Pipeline exceeded global timeout "
                f"({self.timeout}s)"
            )

            ctx.cancel_event.set()

            await self.rollback_pipeline(
                ctx,
                executed_steps,
            )

            return False

        finally:

            self.active.pop(
                task_id,
                None,
            )

    async def rollback_pipeline(
        self,
        ctx: ExecutionContext,
        executed_steps: List[str],
    ) -> None:

        logger.warning(
            "===== BEGIN PIPELINE ROLLBACK ====="
        )

        for step_id in reversed(executed_steps):

            worker = self.workers.get(step_id)

            step = ctx.steps[step_id]

            if worker is None:
                continue

            try:

                await worker.rollback(
                    ctx.task_id,
                    ctx.project,
                )

                step.status = StepStatus.ROLLED_BACK

            except Exception as exc:

                logger.exception(
                    f"Rollback failed for "
                    f"{step_id}: {exc}"
                )

        self.memory.write(
            f"pipeline_result_{ctx.task_id}",
            {
                "status": "FAILED",
                "timestamp": datetime.now(
                    timezone.utc
                ).isoformat(),
                "steps": {
                    sid: asdict(step)
                    for sid, step in ctx.steps.items()
                },
            },
        )

        logger.warning(
            "===== PIPELINE ROLLBACK COMPLETE ====="
        )

    def pipeline_status(
        self,
        task_id: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Return the current execution status of a running pipeline.
        """

        ctx = self.active.get(task_id)

        if ctx is None:
            return None

        return {
            "task_id": ctx.task_id,
            "steps": {
                sid: {
                    "status": step.status.value,
                    "started": step.started,
                    "ended": step.ended,
                    "error": step.error,
                    "metrics": asdict(step.metrics),
                }
                for sid, step in ctx.steps.items()
            },
        }

    def list_workers(self) -> List[str]:
        """
        Return all registered worker IDs.
        """

        return sorted(self.workers.keys())

    def worker_count(self) -> int:
        """
        Return the number of registered workers.
        """

        return len(self.workers)

    def load_pipeline(self) -> List[Dict[str, Any]]:
        """
        Return the active pipeline blueprint.
        """

        return self.pipeline.copy()

    def export_pipeline(
        self,
        output_file: str,
    ) -> None:
        """
        Export pipeline topology to JSON.
        """

        with open(output_file, "w", encoding="utf-8") as fp:
            json.dump(
                self.pipeline,
                fp,
                indent=4,
            )

    def shutdown(self) -> None:
        """
        Gracefully stop all running pipelines.
        """

        logger.info(
            "Shutting down Orchestrator..."
        )

        for ctx in self.active.values():
            ctx.cancel_event.set()

        self.active.clear()

        logger.info(
            "Shutdown complete."
        )

