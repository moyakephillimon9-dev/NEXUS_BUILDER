from core.shared_memory import SharedMemory

from plugins.manager_ai.agent import ManagerAI
from plugins.architect_ai.agent import ArchitectAI


def execute_master_gate_test():

    print("=" * 60)
    print("NEXUS MASTER STRATEGIC GATE TEST")
    print("=" * 60)

    ##########################################################
    # Shared Memory
    ##########################################################

    shared_memory = SharedMemory()

    shared_memory.write("system", "ONLINE")

    ##########################################################
    # Boot AI
    ##########################################################

    manager = ManagerAI(shared_memory)
    architect = ArchitectAI(shared_memory)

    manager.start()
    architect.start()

    manager.register_employee(
        "ARCHITECT-001",
        architect
    )

    ##########################################################
    # TRACK 1
    ##########################################################

    print("\n" + "-" * 60)
    print("TRACK 1 : HIGH RISK PROJECT")
    print("-" * 60)

    unstable_manifest = {

        "complexity_index":95,

        "target_price":10,

        "estimated_cac":50,

        "requires_personal_data":True,

        "public_internet_exposure":True,

        "high_concurrency":True,

        "database_sharding":False
    }

    task_id, approved = manager.formulate_10_step_plan(

        "Build a hyper-tracking speculative application",

        unstable_manifest
    )

    if approved:

        manager.dispatch_swarm_worker(

            task_id,

            "ARCHITECT-001"

        )

    else:

        print("[Pipeline] Execution blocked by Manager AI.")

    ##########################################################
    # TRACK 2
    ##########################################################

    print("\n" + "-" * 60)
    print("TRACK 2 : HEALTHY PROJECT")
    print("-" * 60)

    secure_manifest = {

        "complexity_index":30,

        "target_price":150,

        "estimated_cac":25,

        "requires_personal_data":False,

        "public_internet_exposure":False,

        "high_concurrency":False
    }

    task_id, approved = manager.formulate_10_step_plan(

        "Build a private encrypted local storage tool",

        secure_manifest
    )

    if approved:

        manager.dispatch_swarm_worker(

            task_id,

            "ARCHITECT-001"

        )

    ##########################################################
    # Final Workspace
    ##########################################################

    print("\n" + "=" * 60)

    print("FINAL PROJECT WORKSPACE")

    print("=" * 60)

    manager.show_projects()


if __name__ == "__main__":

    execute_master_gate_test()
