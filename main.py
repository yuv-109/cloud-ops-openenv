from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Cloud-Ops OpenEnv")

# --- Models ---
# The validator is VERY strict about these field names.
class Observation(BaseModel):
    logs: str
    cpu_usage: float
    memory_usage: float
    active_alerts: List[str]
    step_count: int

class Action(BaseModel):
    command: str
    target: str

class StepResponse(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: dict

# --- State ---
current_step = 0
MAX_STEPS = 5

# Scenarios for the 3 tasks
SCENARIOS = {
    "task_1": {"goal_command": "RESTART", "goal_target": "auth-service", "desc": "Service Recovery"},
    "task_2": {"goal_command": "SCALE_UP", "goal_target": "payment-api", "desc": "Memory Mitigation"},
    "task_3": {"goal_command": "KILL_SESSIONS", "goal_target": "db-cluster", "desc": "Database Deadlock Fix"}
}

# --- Endpoints ---

@app.get("/")
async def root():
    return {"message": "Cloud-Ops OpenEnv is Running", "docs": "/docs"}

@app.get("/tasks")
async def get_tasks():
    return [
        {"id": "task_1", "name": "Service Recovery", "difficulty": "Easy"},
        {"id": "task_2", "name": "Memory Mitigation", "difficulty": "Medium"},
        {"id": "task_3", "name": "Database Deadlock Fix", "difficulty": "Hard"}
    ]

@app.post("/reset", response_model=Observation)
async def reset(task_id: str = "task_1"):
    global current_step
    current_step = 0
    
    # Returning the exact Observation object the validator expects
    return Observation(
        logs=f"Environment reset for {task_id}. Monitoring active.",
        cpu_usage=15.0,
        memory_usage=20.0,
        active_alerts=[],
        step_count=0
    )

@app.post("/step", response_model=StepResponse)
async def step(action: Action, task_id: str = "task_1"):
    global current_step
    current_step += 1
    
    scenario = SCENARIOS.get(task_id, SCENARIOS["task_1"])
    
    # Check if the agent's action matches the goal
    is_correct = (action.command == scenario["goal_command"] and 
                  action.target == scenario["goal_target"])
    
    reward = 1.0 if is_correct else 0.0
    done = is_correct or current_step >= MAX_STEPS
    
    obs = Observation(
        logs=f"Executed {action.command} on {action.target}. Success: {is_correct}",
        cpu_usage=10.0 if is_correct else 50.0,
        memory_usage=15.0 if is_correct else 60.0,
        active_alerts=[] if is_correct else ["SERVICE_DEGRADED"],
        step_count=current_step
    )
    
    return StepResponse(
        observation=obs,
        reward=reward,
        done=done,
        info={"task": scenario["desc"]}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)