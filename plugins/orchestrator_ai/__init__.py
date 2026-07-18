from nexus_orchestrator import OrchestratorAI

orchestrator = None


def initialize(shared_memory):
    global orchestrator

    orchestrator = OrchestratorAI(shared_memory)

    # Register AI workers
    try:
        from plugins.planner_ai.agent import PlannerAI

        planner = PlannerAI(shared_memory)
        orchestrator.register_worker("PLANNER-001", planner)
        print("✓ Registered PLANNER-001")
    except Exception as e:
        print("✗ PLANNER-001:", e)

    try:
        from plugins.architect_ai.agent import ArchitectAI

        architect = ArchitectAI(shared_memory)
        orchestrator.register_worker("ARCHITECT-001", 
    architect)
        print("✓ Registered ARCHITECT-001")
    except Exception as e:
        print("✗ ARCHITECT-001:", e)

    try:
        from plugins.coder_ai.agent import CoderAI

        coder = CoderAI(shared_memory)
        orchestrator.register_worker("CODER-001", coder)
        print("✓ Registered CODER-001")
    except Exception as e:
        print("✗ CODER-001:", e)

    try:
        from plugins.reviewer_ai.agent import ReviewerAI

        reviewer = ReviewerAI(shared_memory)
        orchestrator.register_worker("AUDITOR-001", reviewer)
        print("✓ Registered AUDITOR-001")
    except Exception as e:
        print("✗ AUDITOR-001:", e)

    try:
        from plugins.tester_ai.agent import TesterAI

        tester = TesterAI(shared_memory)
        orchestrator.register_worker("TESTER-001", tester)
        print("✓ Registered TESTER-001")
    except Exception as e:
        print("✗ TESTER-001:", e)

    try:
        from plugins.deployment_ai.agent import DeploymentAI

        deployment = DeploymentAI(shared_memory)
        orchestrator.register_worker("DEPLOY-001", deployment)
        print("✓ Registered DEPLOY-001")
    except Exception as e:
        print("✗ DEPLOY-001:", e)

    return orchestrator
