from core.shared_memory import SharedMemory
from plugins.reviewer_ai.agent import ReviewerAI


def execute_reviewer_sandbox_test():

    print("=" * 60)
    print("NEXUS REVIEWER AI VALIDATION")
    print("=" * 60)

    memory = SharedMemory()

    reviewer = ReviewerAI(memory)

    reviewer.start()

    ##########################################################
    # TRACK 1
    ##########################################################

    print("\n" + "-" * 60)
    print("TRACK 1 : VULNERABLE SOURCE")
    print("-" * 60)

    bad_code = """
def process_user_data(user_input):

    return eval(user_input)
"""

    memory.write(

        "active_project_TSK-BAD01",

        {

            "task_id":"TSK-BAD01",

            "goal":"Unsafe Calculator",

            "status":"PROGRAMMING_PHASE",

            "code":{

                "language":"Python",

                "source":bad_code

            }

        }

    )

    reviewer.process_project_task("TSK-BAD01")

    project = memory.read("active_project_TSK-BAD01")

    print("\nReview Summary")

    print(

        f"Quality Score : {project['review']['quality_score']}/100"

    )

    print(

        f"Approved      : {project['review']['approved']}"

    )

    print(

        f"Recommendation: {project['review']['release_recommendation']}"

    )

    print("\nIssues")

    for issue in project["review"]["issues"]:

        print(f"⚠ {issue}")

    ##########################################################
    # TRACK 2
    ##########################################################

    print("\n" + "-" * 60)
    print("TRACK 2 : CLEAN SOURCE")
    print("-" * 60)

    good_code = """
import hashlib

def calculate_secure_hash(payload):

    data = str(payload).encode()

    return hashlib.sha256(data).hexdigest()
"""

    memory.write(

        "active_project_TSK-GOOD02",

        {

            "task_id":"TSK-GOOD02",

            "goal":"Hash Generator",

            "status":"PROGRAMMING_PHASE",

            "code":{

                "language":"Python",

                "source":good_code

            }

        }

    )

    reviewer.process_project_task("TSK-GOOD02")

    project = memory.read("active_project_TSK-GOOD02")

    print("\nReview Summary")

    print(

        f"Quality Score : {project['review']['quality_score']}/100"

    )

    print(

        f"Approved      : {project['review']['approved']}"

    )

    print(

        f"Recommendation: {project['review']['release_recommendation']}"

    )

    print("\nIssues")

    for issue in project["review"]["issues"]:

        print(f"✓ {issue}")

    print("\n" + "=" * 60)


if __name__ == "__main__":

    execute_reviewer_sandbox_test()
