import argparse
import sys
from .loader import load_pipeline, validate_pipeline, LoaderError
from .runner import execute_pipeline
from .reporting import generate_report
from .metrics import export_metrics
from .utils import setup_logging

def main():
    setup_logging() # Configure logging once at CLI entry point

    parser = argparse.ArgumentParser(description="Embedded CI Lab CLI")
    parser.add_argument("--version", action="version", version="embedded-ci-lab 2.3.1")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    run_parser = subparsers.add_parser("run", help="Run a pipeline")
    run_parser.add_argument("--pipeline", required=True, help="Path to the YAML pipeline file")

    validate_parser = subparsers.add_parser("validate", help="Validate a pipeline configuration")
    validate_parser.add_argument("--pipeline", required=True, help="Path to the YAML pipeline file")

    args = parser.parse_args()

    if args.command == "run":
        try:
            pipeline = load_pipeline(args.pipeline)
            validate_pipeline(pipeline)
            
            # Execute pipeline and get detailed results
            pipeline_result = execute_pipeline(pipeline)
            
            # Always generate a report and export metrics
            try:
                report_file = generate_report(pipeline_result)
                metrics_file = export_metrics(pipeline_result)
                print(f"Report generated: {report_file}")
                print(f"Metrics exported: {metrics_file}")
            except Exception as e:
                print(f"Error generating report/metrics: {e}", file=sys.stderr)
            
            if pipeline_result.status == "success":
                sys.exit(0)
            else:
                sys.exit(1)
        except LoaderError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.command == "validate":
        try:
            pipeline = load_pipeline(args.pipeline)
            validate_pipeline(pipeline)
            print(f"Pipeline '{pipeline.name}' is valid.")
            sys.exit(0)
        except LoaderError as e:
            print(f"Validation Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
