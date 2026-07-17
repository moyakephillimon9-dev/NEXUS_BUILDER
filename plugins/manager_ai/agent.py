"""
NEXUS Builder
Manager AI — Swarm Orchestrator

Module ID : MANAGER-001
Version   : 0.2.1
"""

import uuid
from datetime import datetime


class ManagerAI:
    """
    Central coordinator of the NEXUS AI Engineering Company.
    Responsible for project creation, task routing,
    employee management, and workflow orchestration.
    """

    def __init__(self, shared_memory):
        self.memory = shared_memory
        self.employee_registry = {}
        print("[Manager AI] Connected to Shared Memory.")

    def start(self):
        print("[Manager AI] Swarm Control Online.")

    def register_employee(self, employee_id, agent_instance):
        """
        Registers an AI employee.
        """

        employee_id = employee_id.upper()

        self.employee_registry[employee_id] = agent_instance

        print(f"[Manager AI] Registered Employee: {employee_id}")

    def formulate_10_step_plan(self, high_level_goal):

        task_id = f"TSK-{str(uuid.uuid4())[:6].upper()}"

        task_payload = {
            "task_id": task_id,
            "goal": high_level_goal,
            "created_at": datetime.utcnow().isoformat(),
            "status": "ANALYZING_RISKS",
            "assigned_worker": None,
            "architecture": None,
            "code": None,
            "review": None,
            "tests": None,
            "milestones": [
                "1. Market opportunity assessment",
                "2. Strategic risk analysis",
                "3. Software architecture design",
                "4. Development planning",
                "5. Resource allocation",
                "6. Programming phase",
                "7. Code review",
                "8. Testing",
                "9. Deployment preparation",
                "10. Project completion"
            ]
        }

        self.memory.write(
            f"active_project_{task_id}",
            task_payload
        )

        print(f"[Manager AI] Project Created: {task_id}")

        return task_id

    def dispatch_swarm_worker(self, task_id, worker_id):

        worker_id = worker_id.upper()

        project_key = f"active_project_{task_id}"

        project = self.memory.read(project_key)

        if project is None:
            print("[Manager AI] Project not found.")
            return

        if worker_id not in self.employee_registry:
            print(f"[Manager AI] Employee '{worker_id}' not registered.")
            return

        project["assigned_worker"] = worker_id
        project["status"] = "RESOURCE_ALLOCATED"

        self.memory.write(project_key, project)

        print(f"[Manager AI] Dispatching {worker_id}")

        # Future AI employee execution hook.
        # ArchitectAI, ProgrammerAI, TesterAI, etc.
        self.employee_registry[worker_id].process_project_task(task_id)

    def list_employees(self):

        print("\nRegistered Employees")

        if not self.employee_registry:
            print("No employees registered.")
            return

        for employee in self.employee_registry:
            print(f"✓ {employee}")

    def show_projects(self):

        print("\nCurrent Projects")

        self.memory.print_memory()




