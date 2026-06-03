# Data Model: HAR Parser Module

## Entities

### Request Step (`req_NNNN.json`)
Represents a single HTTP request extracted from a HAR entry.

| Field | Type | Description | Validation/Notes |
|-------|------|-------------|-------------------|
| `method` | string | HTTP method (e.g., GET, POST) | Mandatory |
| `url` | string | Full request URL | Mandatory |
| `headers` | Array<{name: string, value: string}> | List of request headers | Mandatory |
| `postData` | object \| null | Data sent in the request body | Optional |
| `queryString` | Array<{name: string, value: string}> \| null | List of query parameters | Optional |

### Response Step (`res_NNNN.json`)
Represents a single HTTP response extracted from a HAR entry.

| Field | Type | Description | Validation/Notes |
|-------|------|-------------|-------------------|
| `status` | integer | HTTP response status code | Mandatory |
| `headers` | Array<{name: string, value: string}> | List of response headers | Mandatory |
| `content` | object | Response body and metadata | Mandatory |
| `content.text` | string | Decoded response body text | Mandatory (decoded from base64 if needed) |
| `content.mimeType` | string | MIME type of the response | Optional |

## Relationships
- A single HAR entry results in exactly one **Request Step** and one **Response Step**.
- Files are linked by their index `NNNN` (e.g., `req_0001.json` and `res_0001.json` belong to the same entry).
