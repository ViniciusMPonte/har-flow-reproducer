# Quickstart: HAR Parser Module

## Overview
The HAR Parser module allows you to decompose a complex HAR archive into a sequence of individual request and response files, making them easier to inspect and modify.

## Installation
*(To be filled after implementation: e.g., `npm install`)*

## Basic Usage

### Parse a HAR file
Run the following command to split a HAR file into a directory of JSON steps:

```bash
har-reproducer parse --har path/to/your/file.har --output ./output-dir
```

### Expected Output
If your HAR file contains 3 entries, the `./output-dir` will contain:
- `req_0001.json` & `res_0001.json`
- `req_0002.json` & `res_0002.json`
- `req_0003.json` & `res_0003.json`

## Examples

### Validating base64 decoding
If a response in the HAR file is base64 encoded, the resulting `res_NNNN.json` will automatically contain the plain-text decoded version in the `content.text` field.

## Troubleshooting
- **File not found**: Ensure the `--har` path is correct.
- **Invalid JSON**: Verify that the input file is a valid HAR archive.
- **Permission denied**: Ensure you have write access to the `--output` directory.
