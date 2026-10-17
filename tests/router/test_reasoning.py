from intelligence_router import router, TaskType
import platform

def test_prometheus():
    print("🧠 Testing Prometheus (DeepSeek-R1) Integration...")
    
    prompt = "Explain the logic of the 'Ship of Theseus' paradox in one sentence."
    
    try:
        # Request REASONING task
        print(f"\n[Input]: {prompt}")
        response = router.generate(prompt, task_type=TaskType.REASONING)
        
        print(f"\n[Response]: {response}")
        print("\n✅ DeepSeek-R1 Test Complete.")
        
    except Exception as e:
        print(f"\n❌ Test Failed: {e}")

if __name__ == "__main__":
    test_prometheus()
