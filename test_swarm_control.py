from core.shared_memory import SharedMemory

from plugins.manager_ai.agent import ManagerAI
from plugins.coder_ai.agent import CoderAI


def run_swarm_orchestration_test():

    print("=" * 60)
    print("NEXUS MULTI-AGENT SWARM VALIDATION")
    print("=" * 60)

    # Boot Shared Memory

    shared_memory = SharedMemory()

    shared_memory.write("system", "ONLINE")

    # Boot Manager AI

    manager = ManagerAI(shared_memory)

    manager.start()

    # Boot Coder AI

    coder = CoderAI(shared_memory)

    coder.start()

    # Register employee

    manager.register_employee(
        employee_id="CODER-001",
        agent_instance=coder
    )

    manager.list_employees()

    # Founder gives project

    project_id = manager.formulate_10_step_plan(
        "Build an isolated micro-service payment API"
    )

    print("\nDispatching Work")
    print("-" * 60)

    manager.dispatch_swarm_worker(
        task_id=project_id,
        worker_id="CODER-001"
    )

    print("\nVerification")
    print("-" * 60)

    manager.show_projects()

    print("=" * 60)


if __name__ == "__main__":
    run_swarm_orchestration_test()
