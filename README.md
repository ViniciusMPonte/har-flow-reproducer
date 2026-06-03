# HAR Flow Reproducer

The HAR Flow Reproducer is a CLI tool designed to decompose HTTP Archive (HAR) files into individual, manageable request and response JSON files. This process simplifies the inspection, modification, and reproduction of specific network flows.

## Features

- **HAR Splitting**: Splits a single `.har` file into pairs of `req_NNNN.json` and `res_NNNN.json` files.
- **Automatic Base64 Decoding**: Detects base64 encoded response bodies and automatically decodes them to plain text.
- **Scalable Indexing**: Supports large HAR files by automatically expanding the file index from 4 to 5 digits when more than 9,999 entries are present.
- **Robust Error Handling**: Provides clear feedback for missing files, malformed JSON, or write permission issues.

## Requirements

- Python 3.11+

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd har-flow-reproducer
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install pydantic pytest pytest-httpx
   ```

## Usage

The tool is executed via the `src/cli/main.py` entry point.

### Split a HAR file
Use the `parse` command to decompose a HAR file into an output directory:

```bash
export PYTHONPATH=.
python3 src/cli/main.py parse --har path/to/your/file.har --output ./output-dir
```

**Arguments**:
- `--har`: Path to the input `.har` file.
- `--output`: Directory where the resulting JSON files will be stored.

### Example Output
If your HAR file contains 3 entries, the output directory will contain:
- `req_0001.json` & `res_0001.json`
- `req_0002.json` & `res_0002.json`
- `req_0003.json` & `res_0003.json`

## Testing

The project uses `pytest` for unit and integration testing.

1. **Ensure you are in the virtual environment**:
   ```bash
   source .venv/bin/activate
   ```

2. **Run all tests**:
   ```bash
   export PYTHONPATH=.
   pytest
   ```

3. **Run specific test suites**:
   - Unit tests: `pytest tests/unit`
   - Integration tests: `pytest tests/integration`
