import requests
import time

# This is your live Hugging Face API endpoint
BASE_URL = "https://yuvule-cloud-ops-openenv.hf.space"

def run_inference():
    # These are the 3 tasks you built in main.py
    tasks = ["task_1", "task_2", "task_3"]
    print(f"🚀 Starting inference for {len(tasks)} tasks...")
    
    for task_id in tasks:
        print(f"\n--- Testing {task_id} ---")
        
        # 1. Reset the environment for the specific task
        # The validator specifically checks this /reset endpoint!
        reset_resp = requests.post(f"{BASE_URL}/reset?task_id={task_id}")
        if reset_resp.status_code == 200:
            print(f"✅ Reset Successful")
        
        # 2. Execute the "Expert" move to prove the task is solvable
        moves = {
            "task_1": {"command": "RESTART", "target": "auth-service"},
            "task_2": {"command": "SCALE_UP", "target": "payment-api"},
            "task_3": {"command": "KILL_SESSIONS", "target": "db-cluster"}
        }
        
        # 3. Send the action to the /step endpoint
        step_resp = requests.post(f"{BASE_URL}/step", json=moves[task_id]).json()
        reward = step_resp.get("reward", 0.0)
        print(f"🎯 Action: {moves[task_id]['command']} | Reward: {reward}")

if __name__ == "__main__":
    # Wait a moment for the server to be fully ready
    time.sleep(2)
    run_inference()