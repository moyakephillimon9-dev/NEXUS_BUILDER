from core.shared_memory import SharedMemory

from plugins.manager_ai.agent import ManagerAI
from plugins.architect_ai.agent import ArchitectAI
from plugins.coder_ai.agent import CoderAI


def run_integrated_nexus_pipeline():

    print("=" * 60)
    print("NEXUS FULL AI ENGINEERING PIPELINE")
    print("=" * 60)

    # Shared Memory

    shared_memory = SharedMemory()

    shared_memory.write("system", "ONLINE")

    # Boot AI Employees

    manager = ManagerAI(shared_memory)
    architect = ArchitectAI(shared_memory)
    coder = CoderAI(shared_memory)

    manager.start()
    architect.start()
    coder.start()

    # Register Employees

    manager.register_employee(
        employee_id="ARCHITECT-001",
        agent_instance=architect
    )

    manager.register_employee(
        employee_id="CODER-001",
        agent_instance=coder
    )

    manager.list_employees()

    # Founder creates project

    project_id = manager.formulate_10_step_plan(
        "Build an isolated local e-commerce API"
    )

    print("\nDispatching Architect AI")
    print("-" * 60)

    manager.dispatch_swarm_worker(
        task_id=project_id,
        worker_id="ARCHITECT-001"
    )

    print("\nDispatching Coder AI")
    print("-" * 60)

    manager.dispatch_swarm_worker(
        task_id=project_id,
        worker_id="CODER-001"
    )

    print("\nFinal Workspace")
    print("-" * 60)

    manager.show_projects()

    print("=" * 60)


if __name__ == "__main__":
    run_integrated_nexus_pipeline()
