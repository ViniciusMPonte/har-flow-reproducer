# CLI Contract: HAR Flow Reproducer

## Command: `parse`

Parses a HAR file and splits it into individual request and response JSON files.

### Usage
`har-reproducer parse --har <file_path> --output <dir_path>`

### Arguments
None

### Options
| Option | Required | Type | Description | Example |
|--------|----------|------|-------------|---------|
| `--har` | Yes | path | Path to the input `.har` file | `--har ./logs/session.har` |
| `--output` | Yes | path | Path to the directory where output files will be written | `--output ./steps` |

### Exit Codes
| Code | Meaning | Description |
|------|---------|-------------|
| `0` | Success | The HAR file was parsed successfully and files were written. |
| `1` | Error | An error occurred (e.g., file not found, invalid JSON, write permission denied). |

### Output Files
For each entry $N$ in the HAR file:
- `req_{NNNN}.json`: Contains the request details.
- `res_{NNNN}.json`: Contains the response details.
- $NNNN$ is the 1-based index zero-padded to 4 digits (e.g., `0001`, `0042`).
