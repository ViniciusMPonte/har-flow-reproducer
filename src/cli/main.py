import argparse
import json
import sys
from pathlib import Path

from src.parser.har_parser import HARParser


def main():
    parser = argparse.ArgumentParser(description="HAR Flow Reproducer - Split HAR files into request/response pairs")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Parse command
    parse_parser = subparsers.add_parser("parse", help="Split a HAR file into individual JSON files")
    parse_parser.add_argument("--har", type=Path, required=True, help="Path to the input HAR file")
    parse_parser.add_argument("--output", type=Path, required=True, help="Output directory for the JSON files")

    args = parser.parse_args()

    if args.command == "parse":
        try:
            if not args.har.exists():
                print(f"Error: HAR file not found at {args.har}", file=sys.stderr)
                sys.exit(1)
            
            parser = HARParser(args.har)
            parser.split_har(args.output)
            print(f"Successfully parsed {args.har} into {args.output}")
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from {args.har}. The file may be malformed.", file=sys.stderr)
            sys.exit(1)
        except PermissionError:
            print(f"Error: Permission denied when writing to {args.output}", file=sys.stderr)
            sys.exit(1)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
