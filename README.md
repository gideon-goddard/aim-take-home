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
- **Lead Time Tracking:**
  - Track and update lead times for components.
  - View lead time reports via CLI and API.
- **Failure Rate Analysis:**
  - Record and analyze failure rates for components.
  - Generate failure rate reports via CLI and API.
- **Allocation Validation:**
  - Validate if inventory allocations meet hardware revision requirements.
  - Check allocation status via CLI and API.

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
- Track and update component lead times (option 17)
- View lead time reports (option 18)
- Record and analyze component failure rates (option 19)
- Generate failure rate reports (option 20)
- Validate inventory allocation for hardware revisions (option 21)

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
  - `POST /components/{component_id}/lead-time` to update lead time
  - `GET /components/{component_id}/lead-time` to view lead time
  - `POST /components/{component_id}/failure-rate` to record failure rate
  - `GET /components/{component_id}/failure-rate` to view failure rate analysis
  - `GET /inventory/` to list all inventory items with optional filters
  - `GET /hardware-revisions/{hwrev_id}/verify-inventory` to check component availability for a hardware revision
  - `GET /hardware-revisions/{hwrev_id}/validate-allocation` to validate allocation for a hardware revision

## Testing
Run the test suite with:
```sh
pytest
```
All CRUD operations and extension features (including cost history tracking, lead time, failure rate, and allocation validation) are covered by unit tests in `test_operations.py`.

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

## Demo
The CLI demo mode showcases all major features with realistic data, including:
- Creating several components (e.g., CPU, RAM, SSD, Power Supply) with initial costs, lead times, and failure rates.
- Adding inventory items for each component, with varying quantities and states (e.g., available, allocated, defective).
- Creating hardware revisions that require specific quantities of each component.
- Updating component costs and tracking cost history.
- Generating inventory and cost history reports.
- Verifying if hardware revision requirements are met by current inventory.
- Tracking and reporting component lead times (e.g., CPUs with 7-day lead time, SSDs with 3-day lead time).
- Recording and analyzing component failure rates (e.g., RAM with 0.5% failure rate, Power Supply with 1% failure rate).
- Validating inventory allocation for hardware revisions (e.g., checking if enough CPUs and RAM are available for a new server build).

**Demo steps:**
1. Add components: CPU, RAM, SSD, Power Supply (with costs, lead times, failure rates).
2. Add inventory: 10 CPUs (available), 20 RAM (available), 5 SSDs (allocated), 2 Power Supplies (defective).
3. Create hardware revision: 'Server v1' (requires 2 CPUs, 4 RAM, 1 SSD, 1 Power Supply).
4. Update CPU cost twice to demonstrate cost history.
5. Generate and display inventory and cost history reports.
6. Verify if 'Server v1' can be built from current inventory.
7. Update and report lead times for all components.
8. Record and analyze failure rates for all components.
9. Validate allocation for 'Server v1' (should fail if not enough available inventory).

Run `python main.py` and select the demo option to see animated output demonstrating these realistic scenarios and all system capabilities.
