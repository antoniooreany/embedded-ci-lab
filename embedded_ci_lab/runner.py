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
        
        attempt = 0
        max_attempts = step.retries + 1
        success = False
        
        step_started_at = datetime.now()
        
        while attempt < max_attempts:
            attempt += 1
            attempt_prefix = f" (attempt {attempt}/{max_attempts})" if step.retries > 0 else ""
            
            logger.info(f"{log_prefix} {step.name} ... {attempt_prefix}")
            
            step_status = "failure" 
            exit_code = -1
            stdout_output = ""
            stderr_output = ""

            try:
                # Use timeout if specified
                timeout = step.timeout_seconds if step.timeout_seconds else None
                result = subprocess.run(step.command, shell=True, capture_output=True, text=True, timeout=timeout)
                stdout_output = result.stdout
                stderr_output = result.stderr
                exit_code = result.returncode
                
                if result.returncode == 0:
                    logger.info(f"{log_prefix} {step.name} ... OK{attempt_prefix}")
                    step_status = "success"
                    success = True
                    break # Success, move to next step
                else:
                    logger.error(f"{log_prefix} {step.name} ... FAIL{attempt_prefix}")
                    logger.error(f"Command '{step.command}' failed with exit code {result.returncode}")
                    if result.stdout:
                        logger.error(f"--- stdout ---\n{result.stdout}")
                    if result.stderr:
                        logger.error(f"--- stderr ---\n{result.stderr}")
                    
            except subprocess.TimeoutExpired as e:
                logger.error(f"{log_prefix} {step.name} ... FAIL (Timeout after {step.timeout_seconds}s){attempt_prefix}")
                step_status = "failure"
                exit_code = 124 
                stdout_output = e.stdout.decode() if e.stdout else ""
                stderr_output = e.stderr.decode() if e.stderr else ""
                logger.error(f"Command '{step.command}' timed out")
            except Exception as e:
                logger.exception(f"{log_prefix} {step.name} ... ERROR: Failed to execute command '{step.command}'{attempt_prefix}")
                step_status = "failure"
            
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

        if not success:
            pipeline_overall_status = "failure"
            break # Move to next step loop, which will break due to failure
            
    pipeline_finished_at = datetime.now()
    
    logger.info(f"Pipeline '{pipeline.name}' completed with status: {pipeline_overall_status}.")
    
    return PipelineResult(
        pipeline_name=pipeline.name,
        started_at=pipeline_started_at,
        finished_at=pipeline_finished_at,
        status=pipeline_overall_status,
        step_results=step_results
    )