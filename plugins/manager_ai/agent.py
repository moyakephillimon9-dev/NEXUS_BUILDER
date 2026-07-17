"""
NEXUS Builder
Manager AI

Module ID : MANAGER-001
Version   : 0.1.0
"""

import uuid
from datetime import datetime


class ManagerAI:
    """
    The first AI employee of NEXUS.
    Responsible for receiving goals and creating projects.
    """

    def __init__(self, shared_memory):
        self.memory = shared_memory
        print("[Manager AI] Connected to Shared Memory")

    def start(self):
        print("[Manager AI] Ready")

    def formulate_10_step_plan(self, high_level_goal):
        """
        Creates a new project entry inside Shared Memory.
        """

        task_id = f"TSK-{str(uuid.uuid4())[:6].upper()}"

        task_payload = {
            "task_id": task_id,
            "goal": high_level_goal,
            "created_at": datetime.utcnow().isoformat(),
            "status": "ANALYZING_RISKS",
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

    def show_projects(self):
        print("\nManager AI Projects")
        self.memory.print_memory()
