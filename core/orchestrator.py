"""
NEXUS Builder
Enterprise Orchestrator

Module ID : ORCHESTRATOR-001
Version   : 2.0.0

Full 16-stage sequential delivery pipeline:

  Research AI → Planner AI → Architect AI → Database AI →
  Coder AI → Design AI → Reviewer AI → Tester AI →
  Security AI → Performance AI → Documentation AI →
  Monitoring AI → Integration AI → DevOps AI →
  Deployment AI → Memory AI
"""

import os

from core.shared_memory import SharedMemory

from plugins.manager_ai.agent       import ManagerAI
from plugins.research_ai.agent      import ResearchAI
from plugins.planner_ai.agent       import PlannerAI
from plugins.architect_ai.agent     import ArchitectAI
from plugins.database_ai.agent      import DatabaseAI
from plugins.coder_ai.agent         import CoderAI
from plugins.design_ai.agent        import DesignAI
from plugins.reviewer_ai.agent      import ReviewerAI
from plugins.tester_ai.agent        import TesterAI
from plugins.security_ai.agent      import SecurityAI
from plugins.performance_ai.agent   import PerformanceAI
from plugins.documentation_ai.agent import DocumentationAI
from plugins.monitoring_ai.agent    import MonitoringAI
from plugins.integration_ai.agent   import IntegrationAI
from plugins.devops_ai.agent        import DevOpsAI
from plugins.deployment_ai.agent    import DeploymentAI
from plugins.memory_ai.agent        import MemoryAI


class Orchestrator:
    """
    NEXUS Enterprise Orchestrator.

    Boots all 17 AI agents, registers them under the ManagerAI
    swarm, then drives the full 16-stage sequential delivery
    pipeline for a given project goal.
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

        # ── Instantiate all workers ────────────────────────────────── #
        self.manager       = ManagerAI(self.shared_memory)
        self.researcher    = ResearchAI(self.shared_memory)
        self.planner       = PlannerAI(self.shared_memory)
        self.architect     = ArchitectAI(self.shared_memory)
        self.database      = DatabaseAI(self.shared_memory)
        self.coder         = CoderAI(self.shared_memory)
        self.designer      = DesignAI(self.shared_memory)
        self.reviewer      = ReviewerAI(self.shared_memory)
        self.tester        = TesterAI(self.shared_memory)
        self.security      = SecurityAI(self.shared_memory)
        self.performance   = PerformanceAI(self.shared_memory)
        self.documenter    = DocumentationAI(self.shared_memory)
        self.monitor       = MonitoringAI(self.shared_memory)
        self.integrator    = IntegrationAI(self.shared_memory)
        self.devops        = DevOpsAI(self.shared_memory)
        self.deployer      = DeploymentAI(self.shared_memory)
        self.memory        = MemoryAI(self.shared_memory)

        print("\n[BOOT] All AI Modules Loaded")

        # ── Start services ─────────────────────────────────────────── #
        self.manager.start()
        self.researcher.start()
        self.planner.start()
        self.architect.start()
        self.database.start()
        self.coder.start()
        self.designer.start()
        self.reviewer.start()
        self.tester.start()
        self.security.start()
        self.performance.start()
        self.documenter.start()
        self.monitor.start()
        self.integrator.start()
        self.devops.start()
        self.deployer.start()
        print("[Memory AI] Semantic Knowledge Engine Ready.")

        # ── Register employees ─────────────────────────────────────── #
        self.manager.register_employee("RESEARCH-001",     self.researcher)
        self.manager.register_employee("PLANNER-001",      self.planner)
        self.manager.register_employee("ARCHITECT-001",    self.architect)
        self.manager.register_employee("DATABASE-001",     self.database)
        self.manager.register_employee("CODER-001",        self.coder)
        self.manager.register_employee("DESIGN-001",       self.designer)
        self.manager.register_employee("REVIEWER-001",     self.reviewer)
        self.manager.register_employee("TESTER-001",       self.tester)
        self.manager.register_employee("SECURITY-001",     self.security)
        self.manager.register_employee("PERFORMANCE-001",  self.performance)
        self.manager.register_employee("DOCS-001",         self.documenter)
        self.manager.register_employee("MONITOR-001",      self.monitor)
        self.manager.register_employee("INTEGRATION-001",  self.integrator)
        self.manager.register_employee("DEVOPS-001",       self.devops)
        self.manager.register_employee("DEPLOY-001",       self.deployer)
        self.manager.register_employee("MEMORY-001",       self.memory)

        print("\n[WORKFORCE STATUS]")
        self.manager.list_employees()

    # ------------------------------------------------------------------ #
    # PIPELINE                                                             #
    # ------------------------------------------------------------------ #

    def run(self, goal: str, operational_parameters: dict | None = None):
        """
        Execute the full NEXUS 16-stage delivery pipeline for *goal*.

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

        # ── STAGE 0 : Research AI ─────────────────────────────────── #

        self._section(0, "Intelligence Research Phase")
        self.manager.dispatch_swarm_worker(task_id, "RESEARCH-001")
        project = self._read(task_id)
        research = project.get("research", {})
        print(f"\nResearch Summary")
        print("-" * 40)
        print(f"Project Type  : {research.get('project_type', 'N/A')}")
        print(f"Complexity    : {research.get('complexity', 'N/A')}")
        print(f"Est. Hours    : {research.get('estimated_hours', 'N/A')}")
        print(f"Verified      : {research.get('verified', False)}")
        print(f"Sources       : {len(research.get('sources', []))}")
        print(f"Concepts      : {', '.join(research.get('concepts', [])[:6])}")

        # ── STAGE 1 : Planner AI ──────────────────────────────────── #

        self._section(1, "Planning Phase")
        self.manager.dispatch_swarm_worker(task_id, "PLANNER-001")
        project = self._read(task_id)
        plan    = project.get("plan", {})
        print(f"\nPlanning Summary")
        print("-" * 40)
        print(f"Status          : {project['status']}")
        print(f"Phases          : {plan.get('total_phases', 'N/A')}")
        print(f"Estimated Hours : {plan.get('estimated_total_hours', 'N/A')}")
        print(f"Strategy        : {plan.get('execution_strategy', 'N/A')}")

        # ── STAGE 2 : Architect AI ────────────────────────────────── #

        self._section(2, "Architecture Phase")
        self.manager.dispatch_swarm_worker(task_id, "ARCHITECT-001")
        project = self._read(task_id)
        arch    = project.get("architecture", {})
        print(f"Architecture Status : {project['status']}")
        print(f"Framework           : {arch.get('framework', 'N/A')}")
        print(f"Database            : {arch.get('database', 'N/A')}")

        # ── STAGE 3 : Database AI ─────────────────────────────────── #

        self._section(3, "Database Schema Phase")
        self.manager.dispatch_swarm_worker(task_id, "DATABASE-001")
        project = self._read(task_id)
        db_data = project.get("database", {})
        print(f"\nDatabase Summary")
        print("-" * 40)
        print(f"Schema Type  : {db_data.get('project_type', 'N/A')}")
        print(f"Tables       : {db_data.get('tables', 'N/A')}")
        print(f"Indexes      : {db_data.get('indexes', 'N/A')}")

        # ── STAGE 4 : Coder AI ────────────────────────────────────── #

        self._section(4, "Development Phase")
        self.manager.dispatch_swarm_worker(task_id, "CODER-001")
        project = self._read(task_id)
        code    = project.get("code")

        if not code:
            print("\n[PIPELINE ERROR] Coder AI failed to generate source code.")
            self.manager.show_projects()
            return

        print(f"\nCode Summary")
        print("-" * 40)
        print(f"Project Type  : {code.get('project_type', 'N/A')}")
        print(f"Language      : {code.get('language', 'N/A')}")
        print(f"Files         : {', '.join(code.get('files', []))}")
        print(f"Source Lines  : {len(code.get('source', '').splitlines())}")
        deps = code.get("requirements", [])
        print(f"Dependencies  : {', '.join(deps) if deps else 'none (stdlib only)'}")

        # ── STAGE 5 : Design AI ───────────────────────────────────── #

        self._section(5, "UI/UX Design Phase")
        self.manager.dispatch_swarm_worker(task_id, "DESIGN-001")
        project = self._read(task_id)
        design  = project.get("design", {})
        print(f"\nDesign Summary")
        print("-" * 40)
        print(f"Tone    : {design.get('palette', {}).get('tone', 'N/A')}")
        print(f"Layout  : {design.get('layout', {}).get('type', 'N/A')}")

        # ── STAGE 6 : Reviewer AI ─────────────────────────────────── #

        self._section(6, "Static Review Phase")
        self.manager.dispatch_swarm_worker(task_id, "REVIEWER-001")
        project = self._read(task_id)
        review  = project["review"]

        print("\nReview Results")
        print("-" * 40)
        print(f"Quality Score  : {review['quality_score']}/100")
        print(f"Approved       : {review['approved']}")
        print(f"Recommendation : {review['release_recommendation']}")
        for issue in review.get("issues", []):
            print(f"  • {issue}")

        if not review["approved"]:
            print("\n[PIPELINE HALTED] Reviewer AI rejected this release.")
            self.manager.show_projects()
            return

        # ── STAGE 7 : Tester AI ───────────────────────────────────── #

        self._section(7, "Runtime Validation Phase")
        self.manager.dispatch_swarm_worker(task_id, "TESTER-001")
        project = self._read(task_id)
        tests   = project["tests"]

        print("\nTest Results")
        print("-" * 40)
        print(f"Passed         : {tests['passed']}")
        print(f"Coverage       : {tests['coverage']} %")
        print(f"Execution Time : {tests['execution_time_ms']} ms")
        print(f"Recommendation : {tests['release_recommendation']}")

        if not tests["passed"]:
            print("\n[PIPELINE HALTED] Runtime validation failed.")
            self.manager.show_projects()
            return

        # ── STAGE 8 : Security AI ─────────────────────────────────── #

        self._section(8, "Security Analysis Phase")
        self.manager.dispatch_swarm_worker(task_id, "SECURITY-001")
        project  = self._read(task_id)
        security = project.get("security", {})

        print("\nSecurity Report")
        print("-" * 40)
        print(f"Security Score : {security.get('security_score', 'N/A')}/100")
        print(f"Risk Level     : {security.get('risk_level', 'N/A')}")
        print(f"Total Findings : {security.get('total_findings', 0)}")
        findings = security.get("findings", [])
        if findings:
            for f in findings:
                print(f"  [{f['severity']}] Line {f['line']} — {f['detail']}")
        else:
            print("  ✓ No vulnerabilities detected.")

        if not security.get("approved", False):
            print("\n[PIPELINE HALTED] Security AI blocked this release.")
            self.manager.show_projects()
            return

        # ── STAGE 9 : Performance AI ──────────────────────────────── #

        self._section(9, "Performance Profiling Phase")
        self.manager.dispatch_swarm_worker(task_id, "PERFORMANCE-001")
        project     = self._read(task_id)
        performance = project.get("performance", {})

        print("\nPerformance Report")
        print("-" * 40)
        print(f"Grade          : {performance.get('performance_grade', 'N/A')}")
        print(f"Avg Complexity : {performance.get('avg_complexity', 'N/A')}")
        print(f"Functions      : {performance.get('function_count', 'N/A')}")
        benchmarks = performance.get("benchmarks", [])
        if benchmarks:
            print("\nBenchmarks")
            for b in benchmarks:
                if b.get("skipped"):
                    print(f"  {b['function']:30s} skipped ({b.get('reason', '')})")
                else:
                    print(f"  {b['function']:30s} avg={b['avg_ms']} ms")

        if not performance.get("approved", False):
            print("[PIPELINE] Performance non-blocking — continuing.")

        # ── STAGE 10 : Documentation AI ───────────────────────────── #

        self._section(10, "Technical Documentation Phase")
        self.manager.dispatch_swarm_worker(task_id, "DOCS-001")
        project = self._read(task_id)
        docs    = project.get("documentation", {})
        print(f"\nDocumentation Summary")
        print("-" * 40)
        for f in docs.get("files_written", []):
            print(f"  ✓ {f}")

        # ── STAGE 11 : Monitoring AI ──────────────────────────────── #

        self._section(11, "Observability Phase")
        self.manager.dispatch_swarm_worker(task_id, "MONITOR-001")
        project = self._read(task_id)
        mon     = project.get("monitoring", {})
        print(f"\nMonitoring Summary")
        print("-" * 40)
        for a in mon.get("artefacts", []):
            print(f"  ✓ {a}")

        # ── STAGE 12 : Integration AI ─────────────────────────────── #

        self._section(12, "Integration Layer Phase")
        self.manager.dispatch_swarm_worker(task_id, "INTEGRATION-001")
        project = self._read(task_id)
        intg    = project.get("integration", {})
        print(f"\nIntegration Summary")
        print("-" * 40)
        for a in intg.get("artefacts", []):
            print(f"  ✓ {a}")
        print(f"  Points : {', '.join(intg.get('integration_points', []))}")

        # ── STAGE 13 : DevOps AI ──────────────────────────────────── #

        self._section(13, "DevOps & Infrastructure Phase")
        self.manager.dispatch_swarm_worker(task_id, "DEVOPS-001")
        project = self._read(task_id)
        devops  = project.get("devops", {})
        print(f"\nDevOps Report")
        print("-" * 40)
        print(f"Readiness Score : {devops.get('readiness_score', 'N/A')}%")
        for a in devops.get("artefacts", []):
            print(f"  ✓ {a}")

        # ── STAGE 14 : Deployment AI ──────────────────────────────── #

        self._section(14, "Enterprise Deployment Phase")
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

        # ── STAGE 15 : Memory AI ──────────────────────────────────── #

        self._section(15, "Knowledge Preservation Phase")
        self.manager.dispatch_swarm_worker(task_id, "MEMORY-001")
        project = self._read(task_id)
        mem_db  = project.get("database", {})

        # ── Final Summary ─────────────────────────────────────────── #

        print("\n" + "=" * 70)
        print("PIPELINE SUMMARY  —  NEXUS INTELLIGENCE PHASE 2")
        print("=" * 70)

        arch    = project.get("architecture", {})
        rev     = project.get("review", {})
        tst     = project.get("tests",  {})
        sec     = project.get("security", {})
        perf    = project.get("performance", {})
        dev     = project.get("devops", {})
        res     = project.get("research", {})
        doc     = project.get("documentation", {})
        intg    = project.get("integration", {})

        print(f"Task ID           : {project['task_id']}")
        print(f"Goal              : {project['goal']}")
        print(f"Project Type      : {res.get('project_type', 'N/A')}")
        print(f"Final Status      : {project['status']}")
        print(f"Health Score      : {project['project_health_score']}")
        print(f"─" * 40)
        print(f"Architecture      : {arch.get('framework', 'N/A')}")
        print(f"Database Schema   : {mem_db.get('tables', 'N/A')} tables")
        print(f"Review Score      : {rev.get('quality_score', 'N/A')}/100")
        print(f"Coverage          : {tst.get('coverage', 'N/A')} %")
        print(f"Security Score    : {sec.get('security_score', 'N/A')}/100")
        print(f"Perf Grade        : {perf.get('performance_grade', 'N/A')}")
        print(f"Docs Written      : {doc.get('total_files', 'N/A')} files")
        print(f"DevOps Readiness  : {dev.get('readiness_score', 'N/A')}%")
        print(f"Integration Points: {', '.join(intg.get('integration_points', []))}")
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
