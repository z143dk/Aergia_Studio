from intelligence_router import router, TaskType
try:
    print(router.generate("Write a one-line tagline for Project Aergia.", task_type=TaskType.CREATIVE))
except Exception as e:
    print(f"Error: {e}")
