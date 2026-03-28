from pydantic import BaseModel, Field
from typing import List, Dict, Any, Literal

class Action(BaseModel):
    # This forces the agent to choose only from these valid commands.
    # Prevents "Creativity" where we don't want it (the API call).
    command: Literal[
        "RESTART", 
        "READ_LOGS", 
        "SCALE_UP", 
        "QUARANTINE_IP", 
        "KILL_SESSIONS"
    ] = Field(
        ..., 
        description="The specific operational command to execute."
    )
    
    target: str = Field(
        ..., 
        description="The service or infrastructure component (e.g., 'auth-service', 'db-cluster')."
    )

class Observation(BaseModel):
    logs: str = Field(..., description="System logs and error messages.")
    cpu_usage: float = Field(..., ge=0, le=100, description="CPU usage percentage (0-100).")
    memory_usage: float = Field(..., ge=0, le=100, description="Memory usage percentage (0-100).")
    active_alerts: List[str] = Field(default_factory=list, description="List of currently active system alerts.")
    step_count: int = Field(..., ge=0, description="Current step number in the episode.")

class StepResponse(BaseModel):
    observation: Observation
    reward: float = Field(..., description="Reward signal (typically 0.0 to 1.0).")
    done: bool = Field(..., description="Whether the episode has ended.")
    info: Dict[str, Any] = Field(default_factory=dict, description="Additional diagnostic metadata.")