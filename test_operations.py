import pytest
from models import Component, Inventory, HardwareRevision
from operations import (
    create_component, get_component, update_component, delete_component,
    create_inventory, get_inventory, update_inventory, delete_inventory,
    create_hardware_revision, get_hardware_revision, update_hardware_revision, delete_hardware_revision
)

def test_component_crud():
    comp = Component(vendor_name="VendorA", manufacturer_name="ManuA")
    created = create_component(comp)
    assert created.id is not None
    fetched = get_component(created.id)
    assert fetched == created
    updated = update_component(created.id, {"vendor_name": "VendorB"})
    assert updated.vendor_name == "VendorB"
    deleted = delete_component(created.id)
    assert deleted is True
    assert get_component(created.id) is None

def test_inventory_crud():
    inv = Inventory(component_id="comp1", state="ordered", quantity=2)
    items = create_inventory(inv)
    assert len(items) == 2
    for item in items:
        assert item.id is not None
        fetched = get_inventory(item.id)
        assert fetched == item
        updated = update_inventory(item.id, {"state": "received"})
        assert updated.state == "received"
        deleted = delete_inventory(item.id)
        assert deleted is True
        assert get_inventory(item.id) is None

def test_hardware_revision_crud():
    hw = HardwareRevision(name="RevA")
    created = create_hardware_revision(hw)
    assert created.id is not None
    fetched = get_hardware_revision(created.id)
    assert fetched == created
    updated = update_hardware_revision(created.id, {"name": "RevB"})
    assert updated.name == "RevB"
    deleted = delete_hardware_revision(created.id)
    assert deleted is True
    assert get_hardware_revision(created.id) is None
