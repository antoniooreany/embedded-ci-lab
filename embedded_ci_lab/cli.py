import argparse
import sys
from .loader import load_pipeline, LoaderError

def main():
    parser = argparse.ArgumentParser(description="Embedded CI Lab CLI")
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="Run a pipeline")
    run_parser.add_argument("--pipeline", required=True, help="Path to the YAML pipeline file")

    args = parser.parse_args()

    if args.command == "run":
        try:
            pipeline = load_pipeline(args.pipeline)
            print(f"Pipeline: {pipeline.name}")
            print(f"Steps: {len(pipeline.steps)}")
        except LoaderError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
