# Feature Specification: HAR Parser Module

**Feature Branch**: `001-har-parser`

**Created**: 2026-06-02

**Status**: Draft

**Input**: User description: "I want to implement the HAR Parser module — the first step of the HAR Flow Reproducer tool. The goal is to take a `.har` file as input and split it into individual, inspectable JSON files, one per request/response pair, written to an output directory."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Parse Valid HAR file (Priority: P1)

As a developer, I want to parse a valid HAR file into separate request/response JSON files, so that I can inspect and modify them individually.

**Why this priority**: Core MVP functionality. Without splitting the HAR file, subsequent steps like token tracking, flow building, and flow reproduction cannot be performed.

**Independent Test**: Can be fully tested by running the command with a valid HAR file containing multiple entries and verifying that 2 x N correctly structured JSON files are produced in the target directory.

**Acceptance Scenarios**:

1. **Given** a valid HAR file `arquivo.har` with 3 entries, and a non-existent output directory `./steps`,
   **When** the developer runs `har-reproducer parse --har arquivo.har --output ./steps`,
   **Then** the output directory `./steps` is created, the command completes successfully with a zero exit status, and `./steps` contains exactly 6 files:
   - `req_0001.json` & `res_0001.json`
   - `req_0002.json` & `res_0002.json`
   - `req_0003.json` & `res_0003.json`

2. **Given** a parsed step file `req_0001.json`,
   **When** a user inspects its contents,
   **Then** the structure is a JSON object containing exactly the request fields: `method`, `url`, `headers`, `postData`, and `queryString`.

3. **Given** a parsed step file `res_0001.json`,
   **When** a user inspects its contents,
   **Then** the structure is a JSON object containing exactly the response fields: `status`, `headers`, and `content`.

---

### User Story 2 - Decode Base64 Encoded Response Content (Priority: P2)

As a developer, I want base64-encoded response content in the HAR file to be automatically decoded to plain text, so that I can easily read and analyze it.

**Why this priority**: Essential for human readability and subsequent token tracking. Many HTTP responses in HAR files are saved with base64 encoding to support binary formats or compression.

**Independent Test**: Can be fully tested by parsing a HAR file with at least one entry having `content.encoding: "base64"` and verifying that the resulting `res_NNNN.json` contains the decoded plain text.

**Acceptance Scenarios**:

1. **Given** a HAR file entry where the response body is `"content": {"encoding": "base64", "text": "eyJoZWxsbyI6ICJ3b3JsZCJ9"}`,
   **When** the command parses the HAR file,
   **Then** the decoded text `{"hello": "world"}` is written in the `text` field under `content` in `res_NNNN.json` and the encoding property is omitted or replaced.

---

### User Story 3 - Graceful Handling of Malformed or Empty Input (Priority: P3)

As a developer, I want the tool to handle malformed or empty HAR files gracefully, so that I understand exactly what went wrong instead of seeing raw code stack traces.

**Why this priority**: Standard usability and robustness requirement to prevent silent failures or confusion when encountering invalid inputs.

**Independent Test**: Can be fully tested by passing a non-existent file, an empty file, or a malformed JSON file to the command and verifying that a clear error message is printed and the exit code is non-zero.

**Acceptance Scenarios**:

1. **Given** no file exists at the specified `--har` path,
   **When** the user runs `har-reproducer parse --har non_existent.har --output ./steps`,
   **Then** the tool prints a clear error message to stderr indicating that the file was not found, does not create any files, and exits with a non-zero status.

2. **Given** the specified HAR file is empty or contains invalid JSON syntax,
   **When** the user runs the command,
   **Then** the tool prints a user-friendly error message to stderr indicating that the file is not a valid JSON/HAR file and exits with a non-zero status.

---

### Edge Cases

- **Existing Output Directory Files**: If the output directory already exists and contains files (e.g. from a previous parse run), the parser overwrites matching files (like `req_0001.json`) and leaves other unrelated files in that directory untouched.
- **Null or Missing Optional Content**: If optional HAR fields like `postData` or response `content.text` are null or missing in the input HAR, the parsed JSON files write these fields as `null` or omit them, without crashing.
- **No Write Permissions**: If the tool does not have permissions to write to the specified output directory, it prints a clear error message to stderr and exits with a non-zero status.
- **Out of Range Step Count**: If the HAR file contains more than 9999 entries (e.g., 10005), the tool preserves lexicographical order for the first 9999 files (`0001` to `9999`) and expands to 5 digits for the remaining files (`10000` to `10005`) without failing.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The CLI tool MUST accept the command syntax `har-reproducer parse --har <file_path> --output <dir_path>`.
- **FR-002**: The tool MUST create the output directory specified by `--output` if it does not already exist.
- **FR-003**: The parser MUST read the input HAR file and iterate over all entries in the `log.entries` array in their exact sequential order.
- **FR-004**: For each entry at index N (where index is 1-based, starting at 1), the system MUST write exactly two JSON files to the output directory:
  - `req_NNNN.json`
  - `res_NNNN.json`
  - NNNN MUST be the index zero-padded to exactly 4 digits (e.g., `0001`, `0042`, `0100`).
- **FR-005**: The request file (`req_NNNN.json`) MUST contain only a JSON object representing the request, containing the following keys from the original HAR entry's request object: `method`, `url`, `headers`, `postData`, and `queryString`.
- **FR-006**: The response file (`res_NNNN.json`) MUST contain only a JSON object representing the response, containing the following keys from the original HAR entry's response object: `status`, `headers`, and `content`.
- **FR-007**: If the input response `content` object has `"encoding": "base64"`, the parser MUST decode the base64 `text` string into its plain text representation, save it as the value of the `text` field, and omit/remove the `encoding` property before writing the JSON file.
- **FR-008**: The tool MUST validate that the input file is a valid JSON and conforms to the HAR format structure (containing `log.entries`). If validation fails, it must print a descriptive error message to `stderr` and exit with status `1`.

### Key Entities

- **Request Step File (`req_NNNN.json`)**: A JSON representation of an HTTP request.
  - *Attributes*: `method` (string), `url` (string), `headers` (array of name/value objects), `postData` (object, optional), `queryString` (array of name/value objects).
- **Response Step File (`res_NNNN.json`)**: A JSON representation of an HTTP response.
  - *Attributes*: `status` (integer), `headers` (array of name/value objects), `content` (object containing decoded `text` string and `mimeType`).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Running the command on a valid HAR file containing N entries consistently produces exactly 2 * N files.
- **SC-002**: 100% of the generated files must be ordered lexicographically and match the order of `log.entries` in the original HAR file.
- **SC-003**: 100% of base64-encoded response contents are correctly decoded into standard human-readable UTF-8 text in the output response files.
- **SC-004**: Any error condition (missing file, invalid JSON, write failure) exits with a status code of 1 and outputs a specific, non-stack-trace error message to stderr.
- **SC-005**: Parsing a standard HAR file containing up to 1,000 entries completes in under 3.0 seconds on standard hardware.

## Assumptions

- **Command invocation**: The parser is invoked as `har-reproducer parse` and options `--har` and `--output` are both mandatory.
- **Index numbering**: Step indexing starts at 1 (`req_0001.json`).
- **Overwriting behavior**: If files with matching names already exist in the target output directory, they are silently overwritten.
- **Standard limits**: HAR files are assumed to fit in memory (typically under 100MB), so memory-efficient streaming/parsing is not strictly required.
- **Encoding default**: The standard output encoding for the files and decoded plain text is UTF-8.
