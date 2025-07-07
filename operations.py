from typing import List, Dict
from models import Component, Inventory, HardwareRevision, Cost
from datetime import datetime

# In-memory stores for demonstration
components_store = {}
inventory_store = {}
hardware_revision_store = {}

# Helper for generating unique IDs
import uuid

def _generate_id(prefix):
    return f"{prefix}-{uuid.uuid4().hex[:8]}"

# CRUD for Component
def create_component(component):
    if not component.id:
        component.id = _generate_id("COMP")
    components_store[component.id] = component
    return component

def get_component(component_id):
    return components_store.get(component_id)

def update_component(component_id, updates):
    comp = components_store.get(component_id)
    if not comp:
        return None
    for k, v in updates.items():
        if hasattr(comp, k):
            setattr(comp, k, v)
    components_store[component_id] = comp
    return comp

def delete_component(component_id):
    return components_store.pop(component_id, None) is not None

def update_component_cost(component_id, new_cost):
    comp = components_store.get(component_id)
    if not comp:
        return None
    # Add to cost history
    if hasattr(comp, 'costs') and comp.costs is not None:
        comp.costs.append(Cost(value=new_cost, date=datetime.now()))
    else:
        comp.costs = [Cost(value=new_cost, date=datetime.now())]
    comp.cost = new_cost
    components_store[component_id] = comp
    return comp

def get_component_cost_history(component_id):
    comp = components_store.get(component_id)
    if not comp or not hasattr(comp, 'costs'):
        return []
    return comp.costs

# CRUD for Inventory
def create_inventory(inventory):
    items = []
    for _ in range(inventory.quantity):
        inv = inventory.copy()
        inv.id = _generate_id("INV")
        inventory_store[inv.id] = inv
        items.append(inv)
    return items

def get_inventory(inventory_id):
    return inventory_store.get(inventory_id)

def update_inventory(inventory_id, updates):
    inv = inventory_store.get(inventory_id)
    if not inv:
        return None
    for k, v in updates.items():
        if hasattr(inv, k):
            setattr(inv, k, v)
    inventory_store[inventory_id] = inv
    return inv

def delete_inventory(inventory_id):
    return inventory_store.pop(inventory_id, None) is not None

def list_inventory(state: str = None, component_id: str = None):
    items = list(inventory_store.values())
    if state:
        items = [item for item in items if item.state == state]
    if component_id:
        items = [item for item in items if item.component_id == component_id]
    return items

# CRUD for HardwareRevision
def create_hardware_revision(hw_rev):
    if not hw_rev.id:
        hw_rev.id = _generate_id("HWREV")
    hardware_revision_store[hw_rev.id] = hw_rev
    return hw_rev

def get_hardware_revision(hwrev_id):
    return hardware_revision_store.get(hwrev_id)

def update_hardware_revision(hwrev_id, updates):
    hw = hardware_revision_store.get(hwrev_id)
    if not hw:
        return None
    for k, v in updates.items():
        if hasattr(hw, k):
            setattr(hw, k, v)
    hardware_revision_store[hwrev_id] = hw
    return hw

def delete_hardware_revision(hwrev_id):
    return hardware_revision_store.pop(hwrev_id, None) is not None

def verify_hardware_revision_inventory(hwrev_id: str):
    hw = hardware_revision_store.get(hwrev_id)
    if not hw:
        return None
    # Each component in hw.components is a dict with at least 'component_id' and 'quantity' (if present)
    missing = []
    for comp in hw.components:
        cid = comp.get('component_id')
        required_qty = comp.get('quantity', 1)
        available_qty = sum(item.quantity for item in inventory_store.values() if item.component_id == cid and item.state in ["on-hand-ready", "allocated", "in-production"])
        if available_qty < required_qty:
            missing.append({"component_id": cid, "required": required_qty, "available": available_qty})
    return missing

def get_lead_time_report():
    # Returns a list of (component_id, estimated_lead_time, actual_lead_time)
    return [
        {
            "component_id": comp.id,
            "estimated_lead_time": comp.estimated_lead_time,
            "actual_lead_time": comp.actual_lead_time
        }
        for comp in components_store.values()
    ]

def get_failure_rate_report(threshold: float = 0.05):
    # Returns components with failure_rate >= threshold
    return [
        {
            "component_id": comp.id,
            "failure_rate": comp.failure_rate
        }
        for comp in components_store.values() if comp.failure_rate is not None and comp.failure_rate >= threshold
    ]

def validate_inventory_allocation(component_id: str, requested_qty: int):
    # Returns True if enough on-hand/ready/allocated/in-production inventory exists
    available_qty = sum(item.quantity for item in inventory_store.values() if item.component_id == component_id and item.state in ["on-hand-ready", "allocated", "in-production"])
    return available_qty >= requested_qty, available_qty

def get_cost_history_report(component_id: str):
    comp = components_store.get(component_id)
    if not comp or not hasattr(comp, 'costs'):
        return []
    return [{"value": c.value, "date": c.date} for c in comp.costs]
