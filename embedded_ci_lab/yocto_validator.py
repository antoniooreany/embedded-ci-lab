import fnmatch
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict

@dataclass
class ValidationResult:
    validation_success: bool
    found_artifacts: Dict[str, str] = field(default_factory=dict)
    missing_artifacts: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

def validate_artifacts(artifacts_dir: str, expected_patterns: Dict[str, List[str]]) -> ValidationResult:
    """
    Checks a directory for expected Yocto-style build artifacts.
    
    :param artifacts_dir: Path to the directory containing artifacts.
    :param expected_patterns: Dictionary where keys are artifact classes 
                              (e.g., 'kernel') and values are lists of 
                              glob patterns (e.g., ['zImage', 'Image']).
    :return: ValidationResult object.
    """
    path = Path(artifacts_dir)
    if not path.exists() or not path.is_dir():
        return ValidationResult(
            validation_success=False,
            warnings=[f"Artifacts directory does not exist or is not a directory: {artifacts_dir}"]
        )

    files = [f.name for f in path.iterdir() if f.is_file()]
    
    found_artifacts: Dict[str, str] = {}
    missing_artifacts: List[str] = []
    
    for artifact_class, patterns in expected_patterns.items():
        found_for_class = []
        for pattern in patterns:
            matched = fnmatch.filter(files, pattern)
            if matched:
                found_for_class.extend(matched)
        
        if found_for_class:
            # If multiple files match a class, we pick the first one but could log a warning
            found_artifacts[artifact_class] = found_for_class[0]
            if len(found_for_class) > 1:
                # Optional: add warning about multiple matches
                pass 
        else:
            missing_artifacts.append(artifact_class)

    success = len(missing_artifacts) == 0
    
    return ValidationResult(
        validation_success=success,
        found_artifacts=found_artifacts,
        missing_artifacts=missing_artifacts
    )
