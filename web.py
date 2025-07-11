from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models import Component, Inventory, HardwareRevision
from operations import (
    create_component, get_component, update_component, delete_component,
    create_inventory, get_inventory, update_inventory, delete_inventory,
    create_hardware_revision, get_hardware_revision, update_hardware_revision, delete_hardware_revision,
    update_component_cost, get_component_cost_history, list_inventory, verify_hardware_revision_inventory,
    get_lead_time_report, get_failure_rate_report, validate_inventory_allocation, get_cost_history_report
)
from typing import Any
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def root():
    return {"message": "AIM Inventory Management API. Visit /docs for Swagger UI."}

@app.post("/components/", response_model=Component)
def api_create_component(component: Component):
    return create_component(component)

@app.get("/components/{component_id}", response_model=Component)
def api_get_component(component_id: str):
    comp = get_component(component_id)
    if not comp:
        raise HTTPException(status_code=404, detail="Component not found")
    return comp

@app.put("/components/{component_id}", response_model=Component)
def api_update_component(component_id: str, updates: dict):
    updated = update_component(component_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Component not found")
    return updated

@app.delete("/components/{component_id}")
def api_delete_component(component_id: str):
    deleted = delete_component(component_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Component not found")
    return {"status": "deleted"}

@app.post("/inventory/", response_model=list[Inventory])
def api_create_inventory(inventory: Inventory):
    return create_inventory(inventory)

@app.get("/inventory/{inventory_id}", response_model=Inventory)
def api_get_inventory(inventory_id: str):
    inv = get_inventory(inventory_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inv

@app.put("/inventory/{inventory_id}", response_model=Inventory)
def api_update_inventory(inventory_id: str, updates: dict):
    updated = update_inventory(inventory_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return updated

@app.delete("/inventory/{inventory_id}")
def api_delete_inventory(inventory_id: str):
    deleted = delete_inventory(inventory_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return {"status": "deleted"}

@app.post("/hardware-revisions/", response_model=HardwareRevision)
def api_create_hardware_revision(hw: HardwareRevision):
    return create_hardware_revision(hw)

@app.get("/hardware-revisions/{hwrev_id}", response_model=HardwareRevision)
def api_get_hardware_revision(hwrev_id: str):
    hw = get_hardware_revision(hwrev_id)
    if not hw:
        raise HTTPException(status_code=404, detail="Hardware revision not found")
    return hw

@app.put("/hardware-revisions/{hwrev_id}", response_model=HardwareRevision)
def api_update_hardware_revision(hwrev_id: str, updates: dict):
    updated = update_hardware_revision(hwrev_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Hardware revision not found")
    return updated

@app.delete("/hardware-revisions/{hwrev_id}")
def api_delete_hardware_revision(hwrev_id: str):
    deleted = delete_hardware_revision(hwrev_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Hardware revision not found")
    return {"status": "deleted"}

@app.post("/components/{component_id}/cost")
def api_update_component_cost(component_id: str, new_cost: float):
    updated = update_component_cost(component_id, new_cost)
    if not updated:
        raise HTTPException(status_code=404, detail="Component not found")
    return updated

@app.get("/components/{component_id}/cost-history")
def api_get_component_cost_history(component_id: str):
    history = get_component_cost_history(component_id)
    return JSONResponse(content=[{"value": c.value, "date": c.date.isoformat()} for c in history])

@app.get("/inventory/")
def api_list_inventory(state: str = None, component_id: str = None):
    items = list_inventory(state=state, component_id=component_id)
    return items

@app.get("/hardware-revisions/{hwrev_id}/verify-inventory")
def api_verify_hardware_revision_inventory(hwrev_id: str):
    result = verify_hardware_revision_inventory(hwrev_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Hardware revision not found")
    return {"missing": result, "ok": not result}

@app.get("/lead-time-report")
def api_lead_time_report():
    return get_lead_time_report()

@app.get("/failure-rate-report")
def api_failure_rate_report(threshold: float = 0.05):
    return get_failure_rate_report(threshold)

@app.get("/allocation-validation/{component_id}")
def api_validate_inventory_allocation(component_id: str, requested_qty: int):
    valid, available = validate_inventory_allocation(component_id, requested_qty)
    return {"valid": valid, "available": available}

@app.get("/cost-history-report/{component_id}")
def api_cost_history_report(component_id: str):
    return get_cost_history_report(component_id)
