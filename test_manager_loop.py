from core.shared_memory import SharedMemory
from plugins.manager_ai.agent import ManagerAI


def run_integration_test():
    print("=" * 60)
    print("NEXUS MANAGER AI INTEGRATION TEST")
    print("=" * 60)

    # Create Shared Memory
    local_memory = SharedMemory()

    local_memory.write("system", "ONLINE")

    # Start Manager AI
    manager = ManagerAI(local_memory)

    manager.start()

    # Simulate Founder command
    project_id = manager.formulate_10_step_plan(
        "Build an isolated local e-commerce API"
    )

    # Read project back from Shared Memory
    retrieved_state = local_memory.read(
        f"active_project_{project_id}"
    )

    print("\nVerification Results")
    print("-" * 60)

    print(f"Project ID : {project_id}")
    print(f"Goal       : {retrieved_state['goal']}")
    print(f"Status     : {retrieved_state['status']}")

    print("\nMilestones")

    for milestone in retrieved_state["milestones"]:
        print(f"✓ {milestone}")

    print("\nShared Memory")

    local_memory.print_memory()

    print("=" * 60)


if __name__ == "__main__":
    run_integration_test()
