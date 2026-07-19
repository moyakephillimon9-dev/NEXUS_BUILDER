"""
NEXUS Builder
Enterprise Orchestrator

Module ID : ORCHESTRATOR-001
Version   : 1.0.0

Wires all AI agents together and drives the sequential
pipeline:

  Planner AI → Architect AI → Coder AI →
  Reviewer AI → Tester AI → Deployment AI
"""

from core.shared_memory import SharedMemory

from plugins.manager_ai.agent import ManagerAI
from plugins.planner_ai.agent import PlannerAI
from plugins.architect_ai.agent import ArchitectAI
from plugins.coder_ai.agent import CoderAI
from plugins.reviewer_ai.agent import ReviewerAI
from plugins.tester_ai.agent import TesterAI
from plugins.deployment_ai.agent import DeploymentAI


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

        self.shared_memory.write("system", "ONLINE")
        self.shared_memory.write("factory_mode", "ENTERPRISE")
        self.shared_memory.write("boot_time", "SYSTEM_INITIALIZED")

        print("\n[BOOT] Shared Memory Initialized")

        # Instantiate all agents
        self.manager    = ManagerAI(self.shared_memory)
        self.planner    = PlannerAI(self.shared_memory)
        self.architect  = ArchitectAI(self.shared_memory)
        self.coder      = CoderAI(self.shared_memory)
        self.reviewer   = ReviewerAI(self.shared_memory)
        self.tester     = TesterAI(self.shared_memory)
        self.deployer   = DeploymentAI(self.shared_memory)

        print("\n[BOOT] All AI Modules Loaded")

        # Start services
        self.manager.start()
        self.planner.start()
        self.architect.start()
        self.coder.start()
        self.reviewer.start()
        self.tester.start()
        self.deployer.start()

        # Register employees
        self.manager.register_employee("PLANNER-001",  self.planner)
        self.manager.register_employee("ARCHITECT-001", self.architect)
        self.manager.register_employee("CODER-001",    self.coder)
        self.manager.register_employee("REVIEWER-001", self.reviewer)
        self.manager.register_employee("TESTER-001",   self.tester)
        self.manager.register_employee("DEPLOY-001",   self.deployer)

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

        # ---- Boot ---------------------------------------------------- #

        self._boot_agents()

        # ---- Strategic Gate ------------------------------------------ #

        print("\n" + "=" * 70)
        print("FOUNDER REQUEST")
        print("=" * 70)
        print(goal)

        task_id, approved = self.manager.formulate_10_step_plan(
            high_level_goal=goal,
            operational_parameters=operational_parameters
        )

        if not approved:
            print("\n[PIPELINE] Execution blocked by Manager AI.")
            self.manager.show_projects()
            return

        print(f"\n[PIPELINE] Strategic Gate Approved : {task_id}")

        # ---- STAGE 0 : Planner AI ------------------------------------ #

        print("\n" + "=" * 70)
        print("[STAGE 0] Planning Phase")
        print("=" * 70)

        self.manager.dispatch_swarm_worker(
            task_id=task_id,
            worker_id="PLANNER-001"
        )

        project = self.shared_memory.read(f"active_project_{task_id}")
        print(f"Planning Status : {project['status']}")

        # ---- STAGE 1 : Architect AI ---------------------------------- #

        print("\n" + "=" * 70)
        print("[STAGE 1] Architecture Phase")
        print("=" * 70)

        self.manager.dispatch_swarm_worker(
            task_id=task_id,
            worker_id="ARCHITECT-001"
        )

        project = self.shared_memory.read(f"active_project_{task_id}")
        print(f"Architecture Status : {project['status']}")

        # ---- STAGE 2 : Coder AI -------------------------------------- #

        print("\n" + "=" * 70)
        print("[STAGE 2] Development Phase")
        print("=" * 70)

        self.manager.dispatch_swarm_worker(
            task_id=task_id,
            worker_id="CODER-001"
        )

        project = self.shared_memory.read(f"active_project_{task_id}")
        print(f"Programming Status : {project['status']}")

        code = project.get("code")

        if not code:
            print("\n[PIPELINE ERROR] Coder AI failed to generate source code.")
            self.manager.show_projects()
            return

        if isinstance(code, dict):
            print("\nGenerated Files")
            for file_name in code.get("files", []):
                print(f"  • {file_name}")
            print(f"\nSource Length : {len(code.get('source', ''))} characters")

        # ---- STAGE 3 : Reviewer AI ----------------------------------- #

        print("\n" + "=" * 70)
        print("[STAGE 3] Static Review Phase")
        print("=" * 70)

        self.manager.dispatch_swarm_worker(
            task_id=task_id,
            worker_id="REVIEWER-001"
        )

        project = self.shared_memory.read(f"active_project_{task_id}")
        review  = project["review"]

        print("\nReview Results")
        print("-" * 40)
        print(f"Quality Score  : {review['quality_score']}")
        print(f"Approved       : {review['approved']}")
        print(f"Recommendation : {review['release_recommendation']}")
        print("\nIssues")

        for issue in review["issues"]:
            print(f"  • {issue}")

        if not review["approved"]:
            print("\n[PIPELINE HALTED] Reviewer AI rejected this release.")
            self.manager.show_projects()
            return

        # ---- STAGE 4 : Tester AI ------------------------------------- #

        print("\n" + "=" * 70)
        print("[STAGE 4] Runtime Validation Phase")
        print("=" * 70)

        self.manager.dispatch_swarm_worker(
            task_id=task_id,
            worker_id="TESTER-001"
        )

        project = self.shared_memory.read(f"active_project_{task_id}")
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

        print("\nDeployment Gate Cleared")
        project["deployment_ready"] = True
        self.shared_memory.write(f"active_project_{task_id}", project)

        # ---- STAGE 5 : Deployment AI --------------------------------- #

        print("\n" + "=" * 70)
        print("[STAGE 5] Enterprise Deployment Phase")
        print("=" * 70)

        self.manager.dispatch_swarm_worker(
            task_id=task_id,
            worker_id="DEPLOY-001"
        )

        project    = self.shared_memory.read(f"active_project_{task_id}")
        deployment = project.get("deployment")

        if deployment is None:
            print("\n[DEPLOYMENT FAILED] Deployment metadata not generated.")
            self.manager.show_projects()
            return

        # ---- Deployment Verification --------------------------------- #

        import os

        print("\nDeployment Verification")
        print("-" * 40)
        print(f"Deployment Folder : {deployment['deployment_path']}")

        for artifact in ["main.py", "requirements.txt", "README.md", "deployment.json"]:
            path = os.path.join(deployment["deployment_path"], artifact)
            mark = "✓" if os.path.exists(path) else "✗"
            print(f"  {mark} {artifact}")

        # ---- Final Summary ------------------------------------------- #

        print("\n" + "=" * 70)
        print("PIPELINE SUMMARY")
        print("=" * 70)

        print(f"Task ID          : {project['task_id']}")
        print(f"Goal             : {project['goal']}")
        print(f"Final Status     : {project['status']}")
        print(f"Health Score     : {project['project_health_score']}")
        print(f"Architecture     : {project['architecture']['framework']}")
        print(f"Review Score     : {project['review']['quality_score']}/100")
        print(f"Coverage         : {project['tests']['coverage']} %")
        print(f"Deployment Ready : {project['deployment_ready']}")
        print(f"Deployment Path  : {deployment['deployment_path']}")

        print("\n" + "=" * 70)
        print("NEXUS ENTERPRISE DELIVERY PIPELINE COMPLETE")
        print("=" * 70)
