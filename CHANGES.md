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

