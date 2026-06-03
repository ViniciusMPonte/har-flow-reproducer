---

description: "Task list for HAR Parser Module implementation"
---

# Tasks: HAR Parser Module

**Input**: Design documents from `/specs/001-har-parser/`

**Prerequisites**: plan.md, spec.md, data-model.md

**Tests**: Tests are mandatory and should be written first to ensure they fail before implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)
 
**Purpose**: Project initialization and basic structure
 
- [X] T001 Create project structure (src/, tests/)
- [X] T002 Initialize Python project with pydantic and pytest dependencies in pyproject.toml
- [X] T003 [P] Configure linting and formatting tools (e.g. ruff)


---

## Phase 2: Foundational (Blocking Prerequisites)
 
**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented
 
- [X] T004 Implement Request/Response Pydantic models in src/parser/models.py
- [X] T005 [P] Implement base64 decoding utility in src/utils/encoding.py
- [X] T006 [P] Implement JSON file writing utilities in src/utils/files.py
- [X] T007 Implement basic CLI argument parsing in src/cli/main.py


**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Parse Valid HAR file (Priority: P1) 🎯 MVP

**Goal**: Split a valid HAR file into individual request/response JSON files.

**Independent Test**: Run `har-reproducer parse --har arquivo.har --output ./steps` and verify 2*N files are created with correct content.

### Tests for User Story 1 (MANDATORY) ⚠️
 
- [X] T008 [P] [US1] Integration test for parsing valid HAR file in tests/integration/test_parse_valid.py


### Implementation for User Story 1
 
- [X] T009 [P] [US1] Implement HAR loading and validation in src/parser/har_parser.py
- [X] T010 [US1] Implement logic to extract and iterate over HAR entries in src/parser/har_parser.py
- [X] T011 [US1] Implement file splitting logic (req_NNNN/res_NNNN) in src/parser/har_parser.py
- [X] T012 [US1] Connect CLI 'parse' command to the parser in src/cli/main.py


**Checkpoint**: User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Decode Base64 Encoded Response Content (Priority: P2)

**Goal**: Automatically decode base64 encoded response content to plain text.

**Independent Test**: Parse a HAR file with base64 content and verify the resulting JSON contains decoded text.

### Tests for User Story 2 (MANDATORY) ⚠️
 
- [X] T013 [P] [US2] Unit test for base64 decoding in tests/unit/test_encoding.py
- [X] T014 [P] [US2] Integration test for base64 decoding in tests/integration/test_decode_base64.py


### Implementation for User Story 2
 
- [X] T015 [US2] Update parser to detect base64 encoding and decode content in src/parser/har_parser.py
- [X] T016 [US2] Implement removal of encoding property from output JSON in src/parser/har_parser.py


**Checkpoint**: User Story 2 should be fully functional and testable independently

---

## Phase 5: User Story 3 - Graceful Handling of Malformed or Empty Input (Priority: P3)

**Goal**: Handle invalid inputs (missing file, malformed JSON) without stack traces.

**Independent Test**: Pass non-existent/malformed file and verify clear error message and non-zero exit status.

### Tests for User Story 3 (MANDATORY) ⚠️
 
- [X] T017 [P] [US3] Integration test for missing/malformed HAR files in tests/integration/test_error_handling.py
 
### Implementation for User Story 3
 
- [X] T018 [US3] Implement file-not-found error handling in src/cli/main.py
- [X] T019 [US3] Implement HAR format validation and error handling in src/parser/har_parser.py
- [X] T020 [US3] Implement write-permission error handling in src/utils/files.py


**Checkpoint**: User Story 3 should be fully functional and testable independently

---

## Phase 6: Polish & Cross-Cutting Concerns
 
**Purpose**: Improvements that affect multiple user stories
 
- [X] T021 Implement 5-digit index expansion for entries > 9999 in src/parser/har_parser.py
- [X] T022 [P] Add comprehensive unit tests for parser logic in tests/unit/test_parser.py
- [X] T023 [P] Run final linting and type checking across the project


---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup
- **User Stories (Phase 3-5)**: All depend on Foundational
- **Polish (Phase 6)**: Depends on all desired user stories

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational
- **User Story 2 (P2)**: Can start after Foundational
- **User Story 3 (P3)**: Can start after Foundational

### Within Each User Story

- Tests MUST be written and fail before implementation.
- Parser logic before CLI integration.

### Parallel Opportunities

- Setup tasks T003 can run in parallel.
- Foundational tasks T005 and T006 can run in parallel.
- Once Foundational is done, US1, US2, and US3 can be worked on in parallel.

---

## Parallel Example: User Story 1

```bash
# Launch test and basic loader in parallel:
Task: "Integration test for parsing valid HAR file in tests/integration/test_parse_valid.py"
Task: "Implement HAR loading and validation in src/parser/har_parser.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → MVP!
3. Add User Story 2 → Test independently
4. Add User Story 3 → Test independently
5. Polish & final validation
