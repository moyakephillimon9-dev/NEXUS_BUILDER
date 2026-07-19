"""
NEXUS Builder
Enterprise Orchestrator

Module ID : ORCHESTRATOR-001
Version   : 1.1.0

Full sequential delivery pipeline:

  Planner AI → Architect AI → Coder AI → Reviewer AI →
  Tester AI → Security AI → Performance AI → DevOps AI →
  Deployment AI
"""

import os

from core.shared_memory import SharedMemory

from plugins.manager_ai.agent     import ManagerAI
from plugins.planner_ai.agent     import PlannerAI
from plugins.architect_ai.agent   import ArchitectAI
from plugins.coder_ai.agent       import CoderAI
from plugins.reviewer_ai.agent    import ReviewerAI
from plugins.tester_ai.agent      import TesterAI
from plugins.security_ai.agent    import SecurityAI
from plugins.performance_ai.agent import PerformanceAI
from plugins.devops_ai.agent      import DevOpsAI
from plugins.deployment_ai.agent  import DeploymentAI


class Orchestrator:
    """
    NEXUS Enterprise Orchestrator.

    Boots all AI agents, registers them under the ManagerAI
    swarm, then drives the full sequential delivery pipeline
    for a given project goal.
    """

    def __init__(self):
        self.shared_memory = SharedMemory()

    # ------------------------------------------------------------------ #
    # BOOT                                                                 #
    # ------------------------------------------------------------------ #

    def _boot_agents(self):

        self.shared_memory.write("system",       "ONLINE")
        self.shared_memory.write("factory_mode", "ENTERPRISE")
        self.shared_memory.write("boot_time",    "SYSTEM_INITIALIZED")

        print("\n[BOOT] Shared Memory Initialized")

        # ── Instantiate ────────────────────────────────────────────── #
        self.manager     = ManagerAI(self.shared_memory)
        self.planner     = PlannerAI(self.shared_memory)
        self.architect   = ArchitectAI(self.shared_memory)
        self.coder       = CoderAI(self.shared_memory)
        self.reviewer    = ReviewerAI(self.shared_memory)
        self.tester      = TesterAI(self.shared_memory)
        self.security    = SecurityAI(self.shared_memory)
        self.performance = PerformanceAI(self.shared_memory)
        self.devops      = DevOpsAI(self.shared_memory)
        self.deployer    = DeploymentAI(self.shared_memory)

        print("\n[BOOT] All AI Modules Loaded")

        # ── Start services ─────────────────────────────────────────── #
        self.manager.start()
        self.planner.start()
        self.architect.start()
        self.coder.start()
        self.reviewer.start()
        self.tester.start()
        self.security.start()
        self.performance.start()
        self.devops.start()
        self.deployer.start()

        # ── Register employees ─────────────────────────────────────── #
        self.manager.register_employee("PLANNER-001",     self.planner)
        self.manager.register_employee("ARCHITECT-001",   self.architect)
        self.manager.register_employee("CODER-001",       self.coder)
        self.manager.register_employee("REVIEWER-001",    self.reviewer)
        self.manager.register_employee("TESTER-001",      self.tester)
        self.manager.register_employee("SECURITY-001",    self.security)
        self.manager.register_employee("PERFORMANCE-001", self.performance)
        self.manager.register_employee("DEVOPS-001",      self.devops)
        self.manager.register_employee("DEPLOY-001",      self.deployer)

        print("\n[WORKFORCE STATUS]")
        self.manager.list_employees()

    # ------------------------------------------------------------------ #
    # PIPELINE                                                             #
    # ------------------------------------------------------------------ #

    def run(self, goal: str, operational_parameters: dict | None = None):
        """
        Execute the full NEXUS delivery pipeline for *goal*.

        Parameters
        ----------
        goal : str
            High-level project description entered by the founder.
        operational_parameters : dict, optional
            Complexity, pricing, risk overrides forwarded to ManagerAI.
        """

        print("\n" + "=" * 70)
        print("NEXUS ENTERPRISE DELIVERY PIPELINE")
        print("=" * 70)

        # ── Boot ──────────────────────────────────────────────────── #

        self._boot_agents()

        # ── Strategic Gate ────────────────────────────────────────── #

        print("\n" + "=" * 70)
        print("FOUNDER REQUEST")
        print("=" * 70)
        print(goal)

        task_id, approved = self.manager.formulate_10_step_plan(
            high_level_goal=goal,
            operational_parameters=operational_parameters,
        )

        if not approved:
            print("\n[PIPELINE] Execution blocked by Manager AI.")
            self.manager.show_projects()
            return

        print(f"\n[PIPELINE] Strategic Gate Approved : {task_id}")

        # ── STAGE 0 : Planner AI ──────────────────────────────────── #

        self._section(0, "Planning Phase")
        self.manager.dispatch_swarm_worker(task_id, "PLANNER-001")
        project = self._read(task_id)
        print(f"Planning Status : {project['status']}")

        plan = project.get("plan", {})
        if plan:
            print(f"Phases          : {plan.get('total_phases')}")
            print(f"Estimated Hours : {plan.get('estimated_total_hours')}")
            print(f"Strategy        : {plan.get('execution_strategy')}")

        # ── STAGE 1 : Architect AI ────────────────────────────────── #

        self._section(1, "Architecture Phase")
        self.manager.dispatch_swarm_worker(task_id, "ARCHITECT-001")
        project = self._read(task_id)
        print(f"Architecture Status : {project['status']}")

        # ── STAGE 2 : Coder AI ────────────────────────────────────── #

        self._section(2, "Development Phase")
        self.manager.dispatch_swarm_worker(task_id, "CODER-001")
        project = self._read(task_id)
        print(f"Programming Status : {project['status']}")

        code = project.get("code")
        if not code:
            print("\n[PIPELINE ERROR] Coder AI failed to generate source code.")
            self.manager.show_projects()
            return

        if isinstance(code, dict):
            print("\nGenerated Files")
            for f in code.get("files", []):
                print(f"  • {f}")
            print(f"Source Length : {len(code.get('source', ''))} characters")

        # ── STAGE 3 : Reviewer AI ─────────────────────────────────── #

        self._section(3, "Static Review Phase")
        self.manager.dispatch_swarm_worker(task_id, "REVIEWER-001")
        project = self._read(task_id)
        review  = project["review"]

        print("\nReview Results")
        print("-" * 40)
        print(f"Quality Score  : {review['quality_score']}/100")
        print(f"Approved       : {review['approved']}")
        print(f"Recommendation : {review['release_recommendation']}")
        for issue in review["issues"]:
            print(f"  • {issue}")

        if not review["approved"]:
            print("\n[PIPELINE HALTED] Reviewer AI rejected this release.")
            self.manager.show_projects()
            return

        # ── STAGE 4 : Tester AI ───────────────────────────────────── #

        self._section(4, "Runtime Validation Phase")
        self.manager.dispatch_swarm_worker(task_id, "TESTER-001")
        project = self._read(task_id)
        tests   = project["tests"]

        print("\nTesting Results")
        print("-" * 40)
        print(f"Passed         : {tests['passed']}")
        print(f"Coverage       : {tests['coverage']} %")
        print(f"Execution Time : {tests['execution_time_ms']} ms")
        print(f"Recommendation : {tests['release_recommendation']}")

        if not tests["passed"]:
            print("\n[PIPELINE HALTED] Runtime validation failed.")
            self.manager.show_projects()
            return

        # ── STAGE 5 : Security AI ─────────────────────────────────── #

        self._section(5, "Security Analysis Phase")
        self.manager.dispatch_swarm_worker(task_id, "SECURITY-001")
        project  = self._read(task_id)
        security = project.get("security", {})

        print("\nSecurity Report")
        print("-" * 40)
        print(f"Security Score : {security.get('security_score', 'N/A')}/100")
        print(f"Risk Level     : {security.get('risk_level', 'N/A')}")
        print(f"Total Findings : {security.get('total_findings', 0)}")
        print(f"  Critical     : {security.get('critical', 0)}")
        print(f"  High         : {security.get('high', 0)}")
        print(f"Recommendation : {security.get('recommendation', 'N/A')}")

        findings = security.get("findings", [])
        if findings:
            print("\nFindings")
            for finding in findings:
                print(f"  [{finding['severity']}] Line {finding['line']} — {finding['detail']}")
        else:
            print("  ✓ No security vulnerabilities detected.")

        if not security.get("approved", False):
            print("\n[PIPELINE HALTED] Security AI blocked this release.")
            self.manager.show_projects()
            return

        # ── STAGE 6 : Performance AI ──────────────────────────────── #

        self._section(6, "Performance Profiling Phase")
        self.manager.dispatch_swarm_worker(task_id, "PERFORMANCE-001")
        project     = self._read(task_id)
        performance = project.get("performance", {})

        print("\nPerformance Report")
        print("-" * 40)
        print(f"Grade          : {performance.get('performance_grade', 'N/A')}")
        print(f"Avg Complexity : {performance.get('avg_complexity', 'N/A')}")
        print(f"Max Complexity : {performance.get('max_complexity', 'N/A')}")
        print(f"Functions      : {performance.get('function_count', 'N/A')}")
        print(f"Recommendation : {performance.get('recommendation', 'N/A')}")

        bottlenecks = performance.get("bottlenecks", [])
        if bottlenecks:
            print(f"  Bottlenecks  : {', '.join(bottlenecks)}")
        else:
            print("  ✓ No performance bottlenecks detected.")

        benchmarks = performance.get("benchmarks", [])
        if benchmarks:
            print("\nBenchmarks")
            for b in benchmarks:
                if b.get("skipped"):
                    print(f"  {b['function']:30s} skipped ({b.get('reason', '')})")
                else:
                    print(
                        f"  {b['function']:30s} "
                        f"best={b['best_ms']} ms  "
                        f"avg={b['avg_ms']} ms  "
                        f"complexity={b['complexity']}"
                    )

        if not performance.get("approved", False):
            print("\n[PIPELINE WARNING] Performance AI flagged optimisation issues.")
            print("[PIPELINE] Continuing — performance is non-blocking.")

        # ── STAGE 7 : DevOps AI ───────────────────────────────────── #

        self._section(7, "DevOps & Infrastructure Phase")
        self.manager.dispatch_swarm_worker(task_id, "DEVOPS-001")
        project = self._read(task_id)
        devops  = project.get("devops", {})

        print("\nDevOps Report")
        print("-" * 40)
        print(f"Readiness Score : {devops.get('readiness_score', 'N/A')}%")
        print(f"Artefacts       : {len(devops.get('artefacts', []))}")
        for a in devops.get("artefacts", []):
            print(f"  ✓ {a}")

        # ── STAGE 8 : Deployment AI ───────────────────────────────── #

        self._section(8, "Enterprise Deployment Phase")

        # Mark ready before dispatch
        project["deployment_ready"] = True
        self.shared_memory.write(f"active_project_{task_id}", project)

        self.manager.dispatch_swarm_worker(task_id, "DEPLOY-001")
        project    = self._read(task_id)
        deployment = project.get("deployment")

        if deployment is None:
            print("\n[DEPLOYMENT FAILED] Deployment metadata not generated.")
            self.manager.show_projects()
            return

        print("\nDeployment Verification")
        print("-" * 40)
        deploy_path = deployment["deployment_path"]
        print(f"Deployment Folder : {deploy_path}")

        for artifact in [
            "main.py", "requirements.txt", "README.md", "deployment.json",
            "Dockerfile", "Makefile", "docker-compose.yml",
        ]:
            full = os.path.join(deploy_path, artifact)
            mark = "✓" if os.path.exists(full) else "✗"
            print(f"  {mark} {artifact}")

        # ── Final Summary ─────────────────────────────────────────── #

        print("\n" + "=" * 70)
        print("PIPELINE SUMMARY")
        print("=" * 70)

        print(f"Task ID           : {project['task_id']}")
        print(f"Goal              : {project['goal']}")
        print(f"Final Status      : {project['status']}")
        print(f"Health Score      : {project['project_health_score']}")
        print(f"Architecture      : {project['architecture']['framework']}")
        print(f"Review Score      : {project['review']['quality_score']}/100")
        print(f"Coverage          : {project['tests']['coverage']} %")
        print(f"Security Score    : {project.get('security', {}).get('security_score', 'N/A')}/100")
        print(f"Perf Grade        : {project.get('performance', {}).get('performance_grade', 'N/A')}")
        print(f"DevOps Readiness  : {project.get('devops', {}).get('readiness_score', 'N/A')}%")
        print(f"Deployment Ready  : {project['deployment_ready']}")
        print(f"Deployment Path   : {deployment['deployment_path']}")

        print("\n" + "=" * 70)
        print("NEXUS ENTERPRISE DELIVERY PIPELINE COMPLETE")
        print("=" * 70)

    # ------------------------------------------------------------------ #
    # Helpers                                                              #
    # ------------------------------------------------------------------ #

    def _section(self, number: int, title: str):
        print(f"\n{'=' * 70}")
        print(f"[STAGE {number}] {title}")
        print("=" * 70)

    def _read(self, task_id: str) -> dict:
        return self.shared_memory.read(f"active_project_{task_id}")
