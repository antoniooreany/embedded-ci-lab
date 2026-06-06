from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class Step:
    name: str
    command: str
    params: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Pipeline:
    name: str
    steps: List[Step] = field(default_factory=list)
