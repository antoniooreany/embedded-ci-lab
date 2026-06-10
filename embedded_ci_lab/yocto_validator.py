import os
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

def validate_artifacts(artifacts_root: str, expected_patterns: Dict[str, List[str]]) -> ValidationResult:
    """
    Checks a directory and its subdirectories for expected Yocto-style build artifacts.

    :param artifacts_root: Path to the directory containing artifacts.
    :param expected_patterns: Dictionary where keys are artifact classes 
                              (e.g., 'kernel') and values are lists of 
                              glob patterns (e.g., ['zImage', 'conf/local.conf']).
    :return: ValidationResult object.
    """
    path = Path(artifacts_root).resolve()
    if not path.exists() or not path.is_dir():
        return ValidationResult(
            validation_success=False,
            warnings=[f"Artifacts directory does not exist or is not a directory: {artifacts_root}"]
        )


    # Get all files recursively, stored as POSIX-style relative paths
    all_files = []
    for f in path.rglob('*'):
        if f.is_file():
            # Exclude .git directory and other common build/temp artifacts
            if ".git" in f.parts:
                continue
            # Use forward slashes for cross-platform pattern matching
            rel_path = str(f.relative_to(path)).replace('\\', '/')
            all_files.append(rel_path)
    
    found_artifacts: Dict[str, str] = {}
    missing_artifacts: List[str] = []
    
    for artifact_class, patterns in expected_patterns.items():
        found_for_class = []
        for pattern in patterns:
            # Match against full relative path OR just the filename for convenience
            for f_rel in all_files:
                filename = os.path.basename(f_rel)
                if fnmatch.fnmatch(f_rel, pattern) or fnmatch.fnmatch(filename, pattern):
                    if f_rel not in found_for_class:
                        found_for_class.append(f_rel)
        
        if found_for_class:
            # Pick the first match for this class
            found_artifacts[artifact_class] = found_for_class[0]
        else:
            missing_artifacts.append(artifact_class)

    success = len(missing_artifacts) == 0
    
    return ValidationResult(
        validation_success=success,
        found_artifacts=found_artifacts,
        missing_artifacts=missing_artifacts
    )
