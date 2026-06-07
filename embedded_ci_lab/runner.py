import subprocess
import sys
import logging
import os # Keep os for os.path.join if needed
from datetime import datetime
from .models import Pipeline, PipelineResult, StepResult
from .loader import LoaderError # Re-using for consistent error handling

logger = logging.getLogger(__name__)

def execute_pipeline(pipeline: Pipeline) -> PipelineResult:
    pipeline_started_at = datetime.now()
    step_results = []
    pipeline_overall_status = "success"

    logger.info(f"Starting pipeline: {pipeline.name}")
    
    total_steps = len(pipeline.steps)
    for i, step in enumerate(pipeline.steps):
        step_number = i + 1
        log_prefix = f"[{step_number}/{total_steps}]"
        logger.info(f"{log_prefix} {step.name} ... ") # Log step start
        
        step_started_at = datetime.now()
        step_status = "failure" # Assume failure until proven success
        exit_code = -1 # Default exit code for execution errors
        stdout_output = ""
        stderr_output = ""

        try:
            result = subprocess.run(step.command, shell=True, capture_output=True, text=True)
            stdout_output = result.stdout
            stderr_output = result.stderr
            exit_code = result.returncode
            
            if result.returncode == 0:
                logger.info(f"{log_prefix} {step.name} ... OK")
                step_status = "success"
            else:
                logger.error(f"{log_prefix} {step.name} ... FAIL")
                pipeline_overall_status = "failure" # Mark pipeline as failed
                logger.error(f"Command '{step.command}' failed with exit code {result.returncode}")
                if result.stdout:
                    logger.error("--- stdout ---")
                    logger.error(result.stdout)
                if result.stderr:
                    logger.error("--- stderr ---")
                    logger.error(result.stderr)
                
        except Exception as e:
            logger.exception(f"{log_prefix} {step.name} ... ERROR: Failed to execute command '{step.command}'")
            pipeline_overall_status = "failure" # Mark pipeline as failed
        
        step_finished_at = datetime.now()
        duration = (step_finished_at - step_started_at).total_seconds()

        step_results.append(StepResult(
            name=step.name,
            command=step.command,
            status=step_status,
            exit_code=exit_code,
            started_at=step_started_at,
            finished_at=step_finished_at,
            duration_seconds=duration,
            stdout=stdout_output,
            stderr=stderr_output
        ))

        # Stop pipeline on failure
        if pipeline_overall_status == "failure":
            break # Exit the step loop
            
    pipeline_finished_at = datetime.now()
    
    logger.info(f"Pipeline '{pipeline.name}' completed with status: {pipeline_overall_status}.")
    
    return PipelineResult(
        pipeline_name=pipeline.name,
        started_at=pipeline_started_at,
        finished_at=pipeline_finished_at,
        status=pipeline_overall_status,
        step_results=step_results
    )