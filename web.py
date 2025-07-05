from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models import Component, Inventory, HardwareRevision
from operations import (
    create_component, get_component, update_component, delete_component,
    create_inventory, get_inventory, update_inventory, delete_inventory,
    create_hardware_revision, get_hardware_revision, update_hardware_revision, delete_hardware_revision,
    update_component_cost, get_component_cost_history
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

@app.put("/components/{component_id}", response_model=ComponentCOMP-fdd5f167)
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
