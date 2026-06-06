import subprocess
import sys
from .models import Pipeline
from .loader import LoaderError # Re-using for consistent error handling

def execute_pipeline(pipeline: Pipeline) -> bool:
    print(f"Starting pipeline: {pipeline.name}\n")
    
    total_steps = len(pipeline.steps)
    for i, step in enumerate(pipeline.steps):
        step_number = i + 1
        print(f"[{step_number}/{total_steps}] {step.name} ... ", end="", flush=True)
        
        try:
            # shell=True is needed to run shell commands like 'echo', 'ls', 'uptime'
            # check=False so we can handle the exit code manually
            result = subprocess.run(step.command, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("OK")
            else:
                print("FAIL")
                print(f"Command '{step.command}' failed with exit code {result.returncode}", file=sys.stderr)
                if result.stdout:
                    print("--- stdout ---", file=sys.stderr)
                    print(result.stdout, file=sys.stderr)
                if result.stderr:
                    print("--- stderr ---", file=sys.stderr)
                    print(result.stderr, file=sys.stderr)
                return False # Stop on first failure
        except Exception as e:
            print("ERROR")
            print(f"Failed to execute command '{step.command}': {e}", file=sys.stderr)
            return False # Stop on execution error
            
    print(f"\nPipeline '{pipeline.name}' completed successfully.")
    return True