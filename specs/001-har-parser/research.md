# Research: HAR Parser Module

## Technology Stack Decision

**Decision**: Node.js / TypeScript

**Rationale**: 
- **JSON Ergonomics**: Native support and seamless integration with TypeScript interfaces make handling complex HAR structures highly efficient and type-safe.
- **I/O Performance**: Node.js's asynchronous non-blocking I/O is ideal for the requirement of writing hundreds or thousands of small JSON files (`req_NNNN.json`, `res_NNNN.json`) quickly.
- **Ecosystem**: Excellent CLI tooling and a strong ecosystem for web-related data processing.

**Alternatives Considered**:
- **Python**: Considered for its data processing capabilities and libraries like `Click` and `Pytest`. However, it was rejected in favor of Node.js due to slightly slower I/O performance for many small files and less idiomatic fit for a tool primarily manipulating JSON web archives.

## Tooling & Libraries

| Category | Tool/Library | Rationale |
|-----------|--------------|-----------|
| **CLI Parsing** | `commander` | Industry standard for Node.js CLI tools; provides easy definition of commands, options, and help text. |
| **JSON Handling** | Native `JSON` | Sufficient and highly optimized for the required scale (<100MB files). |
| **File System** | `fs/promises` | Enables non-blocking file creation and writing, ensuring the 3-second performance goal is met. |
| **Base64 Decoding** | Native `Buffer` | `Buffer.from(text, 'base64')` is the standard and most efficient way to handle base64 in Node.js. |
| **Testing** | `Vitest` | Extremely fast test runner with a Jest-compatible API and native TypeScript support. |
| **Target Platform** | Cross-platform | Node.js ensures the tool runs consistently on Linux, macOS, and Windows. |
