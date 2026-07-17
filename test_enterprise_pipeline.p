"""
NEXUS Builder
Enterprise Integration Test

Module ID : TEST-ENTERPRISE-001
Version   : 1.0.0

Part 1
Enterprise Boot Sequence
"""

import os
import json

from core.shared_memory import SharedMemory
from plugins.manager_ai.agent import ManagerAI
from plugins.planner_ai.agent import PlannerAI
from plugins.architect_ai.agent import ArchitectAI
from plugins.coder_ai.agent import CoderAI
from plugins.reviewer_ai.agent import ReviewerAI
from plugins.tester_ai.agent import TesterAI
from plugins.deployment_ai.agent import DeploymentAI


def run_enterprise_pipeline():

    print("=" * 80)

    # Initialize Shared Memory FIRST
    local_state = SharedMemory()

    local_state.write("system", "ONLINE")
    local_state.write("factory_mode", "ENTERPRISE")
    local_state.write("boot_time", "SYSTEM_INITIALIZED")

    ####################################################################
    # SYSTEM INITIALIZATION
    ####################################################################

    shared_memory = SharedMemory()

    shared_memory.write("system", "ONLINE")
    shared_memory.write("factory_mode", "ENTERPRISE")
    shared_memory.write("boot_time", "SYSTEM_INITIALIZED")

    print("\n[BOOT]")
    print("Shared Memory Initialized")

    ####################################################################
    # DEPLOY CORE AI MODULES
    ####################################################################

    manager = ManagerAI(shared_memory)
    planner = PlannerAI(local_state)
    architect = ArchitectAI(shared_memory)
    coder = CoderAI(shared_memory)
    reviewer = ReviewerAI(shared_memory)
    tester = TesterAI(shared_memory)
    deployer = DeploymentAI(shared_memory)

    print("\n[BOOT]")
    print("All AI Modules Loaded")

    ####################################################################
    # START SERVICES
    ####################################################################

    manager.start()
    planner.start()
    architect.start()
    coder.start()
    reviewer.start()
    tester.start()
    deployer.start()

    ####################################################################
    # REGISTER EMPLOYEE NODES
    ####################################################################

    manager.register_employee(
        "ARCHITECT-001",
        architect
    )

    manager.register_employee(
        "PLANNER-001", planner)

    manager.register_employee(
        "CODER-001",
        coder
    )

    manager.register_employee(
        "REVIEWER-001",
        reviewer
    )

    manager.register_employee(
        "TESTER-001",
        tester
    )

    manager.register_employee(
        "DEPLOY-001",
        deployer
    )

    print("\n[WORKFORCE STATUS]")
    manager.list_employees()

    ####################################################################
    # FOUNDER REQUEST
    ####################################################################

    founder_request = (
        "Build an isolated local e-commerce API"
    )

    operational_manifest = {
        "complexity_index": 20.0,
        "target_price": 120.0,
        "estimated_cac": 15.0,
        "requires_personal_data": False,
        "public_internet_exposure": False,
        "high_concurrency": False,
        "database_sharding": False
    }

    print("\n" + "=" * 80)
    print("FOUNDER REQUEST")
    print("=" * 80)
    print(founder_request)

    task_id, approved = manager.formulate_10_step_plan(
        high_level_goal=founder_request,
        operational_parameters=operational_manifest
    )

    if not approved:
        print("\n[PIPELINE]")
        print("Execution blocked by Manager AI.")
        manager.show_projects()
        return

    print("\n[PIPELINE]")
    print(f"Strategic Gate Approved : {task_id}")

    ####################################################################
    # PART 2 STARTS HERE
    ####################################################################

    ####################################################################
    # ENTERPRISE EXECUTION PIPELINE
    ####################################################################

    print("\n" + "=" * 80)
    print("ENTERPRISE EXECUTION PIPELINE")
    print("=" * 80)

    ###############################################################
    # STAGE 1
    ###############################################################

    print("\n[STAGE 1]")
    print("Architecture Phase")

    manager.dispatch_swarm_worker(
        task_id=task_id,
        worker_id="ARCHITECT-001"
    )

    project = shared_memory.read(f"active_project_{task_id}")

    print("Architecture Status :", project["status"])

    ###############################################################
    # STAGE 2
    ###############################################################

    print("\n[STAGE 2]")
    print("Development Phase")

    manager.dispatch_swarm_worker(
        task_id=task_id,
        worker_id="CODER-001"
    )

    project = shared_memory.read(f"active_project_{task_id}")

    print("Programming Status :", project["status"])

    ###############################################################
    # VERIFY CODE ARTIFACT
    ###############################################################

    code = project.get("code")

    if not code:
        print("[PIPELINE ERROR]")
        print("Coder AI failed to generate source code.")
        return

    if isinstance(code, dict):
        print("\nGenerated Files")

        for file_name in code.get("files", []):
            print(" •", file_name)

        print("\nSource Length :", len(code.get("source", "")), "characters")

    ###############################################################
    # STAGE 3
    ###############################################################

    print("\n[STAGE 3]")
    print("Static Review Phase")

    manager.dispatch_swarm_worker(
        task_id=task_id,
        worker_id="REVIEWER-001"
    )

    project = shared_memory.read(f"active_project_{task_id}")

    review = project["review"]

    print("\nReview Results")
    print("------------------------------")
    print("Quality Score :", review["quality_score"])
    print("Approved      :", review["approved"])
    print("Recommendation:", review["release_recommendation"])

    print("\nIssues")

    for issue in review["issues"]:
        print(" •", issue)

    ###############################################################
    # REVIEW GATE
    ###############################################################

    if not review["approved"]:

        print("\nPIPELINE HALTED")
        print("Reviewer AI rejected this release.")

        manager.show_projects()

        return

    ###############################################################
    # STAGE 4
    ###############################################################

    print("\n[STAGE 4]")
    print("Runtime Validation Phase")

    manager.dispatch_swarm_worker(
        task_id=task_id,
        worker_id="TESTER-001"
    )

    project = shared_memory.read(f"active_project_{task_id}")

    tests = project["tests"]

    print("\nTesting Results")
    print("------------------------------")
    print("Passed        :", tests["passed"])
    print("Coverage      :", tests["coverage"], "%")
    print("Execution Time:", tests["execution_time_ms"], "ms")
    print("Recommendation:", tests["release_recommendation"])

    ###############################################################
    # TEST GATE
    ###############################################################

    if not tests["passed"]:

        print("\nPIPELINE HALTED")
        print("Runtime validation failed.")

        manager.show_projects()

        return

    ###############################################################
    # PREPARE DEPLOYMENT
    ###############################################################

    print("\nDeployment Gate Cleared")

    project["deployment_ready"] = True

    shared_memory.write(
        f"active_project_{task_id}",
        project
    )

    ####################################################################
    # PART 3 STARTS HERE
    ####################################################################

    ####################################################################
    # ENTERPRISE DEPLOYMENT PHASE
    ####################################################################

    print("\n" + "=" * 80)
    print("STAGE 5")
    print("Enterprise Deployment Pipeline")
    print("=" * 80)

    manager.dispatch_swarm_worker(
        task_id=task_id,
        worker_id="DEPLOY-001"
    )

    project = shared_memory.read(
        f"active_project_{task_id}"
    )

    deployment = project.get("deployment")

    if deployment is None:

        print("\nDEPLOYMENT FAILED")
        print("Deployment metadata not generated.")

        manager.show_projects()

        return

    ####################################################################
    # VERIFY DEPLOYMENT ARTIFACTS
    ####################################################################

    print("\nDeployment Verification")
    print("-" * 40)

    deployment_path = deployment["deployment_path"]

    print("Deployment Folder")
    print(deployment_path)

    artifacts = [
        "main.py",
        "requirements.txt",
        "README.md",
        "deployment.json"
    ]

    print("\nArtifact Verification")

    for artifact in artifacts:

        artifact_path = os.path.join(
            deployment_path,
            artifact
        )

        if os.path.exists(artifact_path):
            print(f"✓ {artifact}")
        else:
            print(f"✗ {artifact}")

    ####################################################################
    # VERIFY PROJECT VAULT
    ####################################################################

    print("\nVault Verification")
    print("-" * 40)

    archive = deployment["archive"]

    if os.path.exists(archive):

        print("✓ Archive Created")

        with open(archive) as f:

            archive_data = json.load(f)

        print("Archive Task :", archive_data["task_id"])
        print("Archive Goal :", archive_data["goal"])

    else:

        print("✗ Archive Missing")

    ####################################################################
    # VERIFY MANIFEST
    ####################################################################

    print("\nRelease Manifest")
    print("-" * 40)

    manifest = deployment["manifest"]

    print("Version     :", manifest["version"])
    print("Checksum    :", manifest["checksum"])
    print("Generated   :", manifest["generated_at"])

    ####################################################################
    # FINAL SUMMARY
    ####################################################################

    print("\n" + "=" * 80)
    print("ENTERPRISE PIPELINE SUMMARY")
    print("=" * 80)

    print("Task ID")
    print("  ", project["task_id"])

    print("\nGoal")
    print("  ", project["goal"])

    print("\nFinal Status")
    print("  ", project["status"])

    print("\nHealth Score")
    print("  ", project["project_health_score"])

    print("\nArchitecture")
    print("  ", project["architecture"]["framework"])

    print("\nReview Score")
    print("  ", project["review"]["quality_score"])

    print("\nCoverage")
    print("  ", project["tests"]["coverage"], "%")

    print("\nDeployment Ready")
    print("  ", project["deployment_ready"])

    print("\nDeployment Complete")
    print("  ", project.get("deployment_complete", False))

    ####################################################################
    # FINAL ECOSYSTEM REPORT
    ####################################################################

    print("\n" + "=" * 80)
    print("FINAL ECOSYSTEM STATE")
    print("=" * 80)

    manager.show_projects()

    ####################################################################
    # PIPELINE COMPLETE
    ####################################################################

    print("\n" + "=" * 80)
    print("NEXUS SOFTWARE FACTORY")
    print("Enterprise Delivery Pipeline Complete")
    print("=" * 80)


if __name__ == "__main__":
    run_enterprise_pipeline()
