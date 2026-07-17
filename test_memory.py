from core.shared_memory import SharedMemory

memory = SharedMemory()

memory.write("task", "Build Manager AI")

memory.write("status", "Pending")

memory.print_memory()

print()

print("Task:", memory.read("task"))

print("Status:", memory.read("status"))

