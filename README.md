# AIM Hardware Inventory Management System

## Overview
This project is a prototype hardware inventory management system for AIM, designed to demonstrate clean code, validation, CRUD operations, and both CLI and web-based user interfaces. It is built with Python, Pydantic, and FastAPI, and uses in-memory storage for simplicity.

## Features
- **Data Models:** Components, Inventory, and Hardware Revisions with validation (Pydantic).
- **CRUD Operations:** Full create, read, update, and delete for all entities.
- **State Tracking:** Inventory items track their state and can be updated.
- **User Interfaces:**
  - **CLI:** Menu-driven command-line interface (`main.py`).
  - **Web API:** FastAPI app (`web.py`) with OpenAPI docs at `/docs`.
- **Testing:** Unit tests for all CRUD operations (`test_operations.py`).
- **Extensible:** Structure allows for easy addition of features like lead time tracking, failure rate analysis, allocation validation, or cost history.
- **Component Cost History Tracking:**
  - Every time a component's cost is updated, the change is recorded in its cost history.
  - You can view the full cost history for any component via both the CLI and the web API.
  - Automated tests verify that cost history tracking works as expected.
- **Inventory Reporting:**
  - CLI option 15 and the `/inventory/` API endpoint list all inventory items, with optional filters by state or component.
- **Hardware Revision Verification:**
  - CLI option 16 and the `/hardware-revisions/{hwrev_id}/verify-inventory` API endpoint check if all required components for a hardware revision are available in inventory.

## Setup
1. **Clone the repository** and navigate to the project folder.
2. **Create and activate a virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```sh
   pip install fastapi uvicorn pydantic pytest
   ```

## Usage
### Command-Line Interface (CLI)
Run the CLI to manage inventory interactively:
```sh
python main.py
```
Follow the on-screen menu to add, view, update, or delete components, inventory, and hardware revisions.

**New options:**
- Update a component's cost (option 13)
- View a component's cost history (option 14)
- Generate inventory reports (option 15)
- Verify hardware revision inventory (option 16)

### Web API (FastAPI)
Start the FastAPI server:
```sh
python -m uvicorn web:app --reload
```
- Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the interactive Swagger UI.
- Use the API endpoints to manage all entities.
- **New endpoints:**
  - `POST /components/{component_id}/cost` to update a component's cost
  - `GET /components/{component_id}/cost-history` to view cost history
  - `GET /inventory/` to list all inventory items with optional filters
  - `GET /hardware-revisions/{hwrev_id}/verify-inventory` to check component availability for a hardware revision

## Testing
Run the test suite with:
```sh
pytest
```
All CRUD operations and extension features (including cost history tracking) are covered by unit tests in `test_operations.py`.

## Design Decisions & Assumptions
- **In-memory storage** is used for demonstration; no database is required.
- **Pydantic** provides validation and type safety for all models.
- **No authentication** is implemented, as the focus is on core functionality.
- **Extensible structure:** New features can be added by extending models and operations.

## Issues Fixed
- Naming consistency (snake_case)
- Validation for non-negative failure rates and positive inventory quantity
- Safe list defaults with `Field(default_factory=list)`
- Removed mutable default arguments
- Synchronous CRUD functions for compatibility

## How to Extend
- Add new fields or validation to models in `models.py`.
- Implement new business logic in `operations.py`.
- Add new CLI menu options or API endpoints as needed.
