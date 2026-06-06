import argparse
import sys
from .loader import load_pipeline, validate_pipeline, LoaderError

def main():
    parser = argparse.ArgumentParser(description="Embedded CI Lab CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    run_parser = subparsers.add_parser("run", help="Run a pipeline")
    run_parser.add_argument("--pipeline", required=True, help="Path to the YAML pipeline file")

    validate_parser = subparsers.add_parser("validate", help="Validate a pipeline configuration")
    validate_parser.add_argument("--pipeline", required=True, help="Path to the YAML pipeline file")

    args = parser.parse_args()

    if args.command == "run":
        try:
            pipeline = load_pipeline(args.pipeline)
            print(f"Pipeline: {pipeline.name}")
            print(f"Steps: {len(pipeline.steps)}")
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
