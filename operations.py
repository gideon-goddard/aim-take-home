from typing import List, Dict
from models import Component, Inventory, HardwareRevision

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
