## Commit 1
1. Naming Consistency and Pydantic Best Practices
Changed field names to use snake_case (e.g., component_id, vendor_name) for Python convention and consistency.
Used Optional and provided default values for optional fields.
Used Field(default_factory=list) for list fields to avoid mutable default arguments (important for Pydantic models).
2. Validation
Added a Pydantic @validator to Component for failure_rate to ensure it is non-negative.
Added a @validator to Inventory for quantity to ensure it is at least 1.
3. Type Annotations and Defaults
Made sure all fields have clear type annotations and reasonable defaults.
Set optional fields to None or a default value as appropriate.
4. Model Improvements
Ensured all list fields use Field(default_factory=list) for safe default values.
Made fields like actual_lead_time, failure_rate, and pre_setup_required optional with defaults, reflecting that they may not always be provided.
5. Code Comments and Structure
Added comments to indicate where real logic (e.g., ID generation, persistence) should be implemented in the future.
Cleaned up the code for readability and maintainability.
6. No Business Logic Changes Yet
The CRUD and state update functions are still placeholders, but now ready for further implementation.

## Commit 2
We were directly editing the README, moved code to two seperate Python files for models and operations.


## Commit 3
CRUD operations for components, inventory, and hardware revisions are now implemented in operations.py using in-memory stores. Type annotations and async were removed to resolve errors, so all functions are now synchronous and compatible with plain Python.

## Commit 4
- Implemented pytest-based unit tests for all CRUD operations in test_operations.py, ensuring correct creation, retrieval, update, and deletion of all entities.
- Verified that all tests pass, confirming the correctness of the CRUD logic.

## Commit 5
- Added a menu-driven command-line interface (CLI) in `main.py` for managing components, inventory, and hardware revisions interactively.
- Implemented a FastAPI web interface in `web.py` with full CRUD endpoints for all entities, including OpenAPI/Swagger documentation at `/docs`.
- Added a root endpoint to the FastAPI app that provides a welcome message and directs users to the API documentation.
- Both interfaces use the same in-memory backend and models for consistency.
- Provided instructions for running both the CLI and web server in the new README.md.
- Added a comprehensive README.md with setup, usage, testing, design decisions, and extension instructions.

## Commit 6
- Extended the system with component cost history tracking:
  - Added backend logic to update a component's cost and record every change in its cost history.
  - Added functions to retrieve the cost history for any component.
  - Exposed these features in both the CLI (options 13 and 14) and the FastAPI web interface (`/components/{component_id}/cost` and `/components/{component_id}/cost-history`).

## Commit 7
- Added automated test for component cost history tracking in `test_operations.py`.
  - Verifies that multiple cost updates are recorded and retrievable in the correct order.
  - Ensures the extension feature is robust and covered by tests.
- All tests pass, confirming the correctness of the new feature and overall system stability.

## Commit 8
Simply added timing to CLI demo to make it slightly more animated.

## Commit 9
- Added comprehensive Pydantic validation to all models:
  - Enforced non-empty strings for names, IDs, and URLs using @field_validator and mode='before' for Pydantic v2 compatibility.
  - Non-negative checks for costs, lead times, and failure rates.
  - URL validation for order links.
  - State validation for inventory.
  - Quantity must be positive.
  - Optional string fields (like serial_number) must not be empty if provided.
- Updated all validators to use @field_validator and the new info parameter as required by Pydantic v2.
- Added and verified tests for all validation logic; all tests pass, confirming robust error handling for invalid input.
- Models are now robust against invalid data and provide clear error messages for invalid input.

## Commit 10
- Cleaned up .gitignore to ensure all Python cache files, virtual environments, and test cache directories are ignored:
  - Added __pycache__/, *.pyc, venv/, .venv/, and .pytest_cache/ to .gitignore.
  - Confirmed that no cache or environment files are tracked by git.
- The repository now only tracks source code and documentation files relevant to the project.

## Commit 11
- Fixed a typo in the FastAPI update component endpoint's response_model argument (was 'ComponentCOMP-fdd5f167', now correctly 'Component').
- This resolves a runtime error in the web API and ensures the update endpoint works as intended.

## Commit 12
- Added inventory reporting and hardware revision verification features:
  - Implemented backend functions to list all inventory (with optional filters) and to verify if a hardware revision's required components are available in inventory.
  - Added CLI options 15 (list inventory) and 16 (verify hardware revision).
  - Added FastAPI endpoints `/inventory/` (GET) and `/hardware-revisions/{hwrev_id}/verify-inventory` (GET).
  - Added tests for both features in `test_operations.py`.
  - Extended the CLI demo to showcase both features.
- All assignment requirements for inventory state transitions, reporting, and hardware revision verification are now fully met.

