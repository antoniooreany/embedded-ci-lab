from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional

@dataclass
class Step:
    name: str
    command: Optional[str] = None
    type: str = "shell"
    params: Dict[str, Any] = field(default_factory=dict)
    timeout_seconds: Optional[int] = None
    memory_limit_mb: Optional[float] = None
    memory_warn_mb: Optional[float] = None
    retries: int = 0

@dataclass
class Pipeline:
    name: str
    steps: List[Step] = field(default_factory=list)

@dataclass
class StepResult:
    name: str
    command: str
    status: str # "success" or "failure"
    exit_code: int
    started_at: datetime
    finished_at: datetime
    duration_seconds: float
    stdout: str
    stderr: str
    max_memory_mb: float
    retry_count: int
    warnings: List[str] = field(default_factory=list)

@dataclass
class PipelineResult:
    pipeline_name: str
    started_at: datetime
    finished_at: datetime
    status: str # "success" or "failure"
    step_results: List[StepResult] = field(default_factory=list)
