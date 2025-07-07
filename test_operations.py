import pytest
from models import Component, Inventory, HardwareRevision
from operations import (
    create_component, get_component, update_component, delete_component,
    create_inventory, get_inventory, update_inventory, delete_inventory,
    create_hardware_revision, get_hardware_revision, update_hardware_revision, delete_hardware_revision,
    update_component_cost, get_component_cost_history,
    list_inventory, verify_hardware_revision_inventory,
    get_lead_time_report, get_failure_rate_report, validate_inventory_allocation, get_cost_history_report
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

def test_component_cost_history():
    comp = Component(vendor_name="VendorA", manufacturer_name="ManuA")
    created = create_component(comp)
    # Initial cost update
    update_component_cost(created.id, 100.0)
    update_component_cost(created.id, 150.0)
    update_component_cost(created.id, 200.0)
    history = get_component_cost_history(created.id)
    assert len(history) == 3
    assert history[0].value == 100.0
    assert history[1].value == 150.0
    assert history[2].value == 200.0
    # Clean up
    delete_component(created.id)

def test_component_validation():
    import pytest
    from pydantic import ValidationError
    # Empty vendor_name
    with pytest.raises(ValidationError):
        Component(vendor_name="", manufacturer_name="ManuA")
    # Negative actual_lead_time
    with pytest.raises(ValidationError):
        Component(vendor_name="A", manufacturer_name="B", actual_lead_time=-1)
    # Invalid order_link
    with pytest.raises(ValidationError):
        Component(vendor_name="A", manufacturer_name="B", order_link="ftp://badurl")
    # Negative cost
    with pytest.raises(ValidationError):
        Component(vendor_name="A", manufacturer_name="B", cost=-5)
    # Negative failure_rate
    with pytest.raises(ValidationError):
        Component(vendor_name="A", manufacturer_name="B", failure_rate=-0.1)


def test_inventory_validation():
    import pytest
    from pydantic import ValidationError
    # Empty component_id
    with pytest.raises(ValidationError):
        Inventory(component_id="", state="ordered")
    # Invalid state
    with pytest.raises(ValidationError):
        Inventory(component_id="A", state="not-a-state")
    # Zero quantity
    with pytest.raises(ValidationError):
        Inventory(component_id="A", state="ordered", quantity=0)
    # Empty serial_number
    with pytest.raises(ValidationError):
        Inventory(component_id="A", state="ordered", serial_number=" ")


def test_hardware_revision_validation():
    import pytest
    from pydantic import ValidationError
    # Empty name
    with pytest.raises(ValidationError):
        HardwareRevision(name="")

def test_list_inventory():
    comp = Component(vendor_name="VendorA", manufacturer_name="ManuA")
    created = create_component(comp)
    inv1 = Inventory(component_id=created.id, state="ordered", quantity=1)
    inv2 = Inventory(component_id=created.id, state="received", quantity=2)
    create_inventory(inv1)
    create_inventory(inv2)
    all_items = list_inventory()
    assert any(item.state == "ordered" for item in all_items)
    filtered = list_inventory(state="received")
    assert all(item.state == "received" for item in filtered)
    filtered_by_comp = list_inventory(component_id=created.id)
    assert all(item.component_id == created.id for item in filtered_by_comp)
    # Clean up
    delete_component(created.id)

def test_verify_hardware_revision_inventory():
    comp = Component(vendor_name="VendorA", manufacturer_name="ManuA")
    created = create_component(comp)
    inv = Inventory(component_id=created.id, state="on-hand-ready", quantity=2)
    create_inventory(inv)
    hw = HardwareRevision(name="RevA", components=[{"component_id": created.id, "quantity": 1}])
    created_hw = create_hardware_revision(hw)
    result = verify_hardware_revision_inventory(created_hw.id)
    assert result == []  # All required components available
    # Now test missing
    hw2 = HardwareRevision(name="RevB", components=[{"component_id": created.id, "quantity": 10}])
    created_hw2 = create_hardware_revision(hw2)
    result2 = verify_hardware_revision_inventory(created_hw2.id)
    assert result2 and result2[0]["required"] == 10
    # Clean up
    delete_component(created.id)
    delete_hardware_revision(created_hw.id)
    delete_hardware_revision(created_hw2.id)

def test_lead_time_and_failure_rate_and_allocation_and_cost_history():
    comp = Component(vendor_name="VendorA", manufacturer_name="ManuA", estimated_lead_time="5d", actual_lead_time=7, failure_rate=0.1)
    created = create_component(comp)
    update_component_cost(created.id, 100)
    update_component_cost(created.id, 200)
    inv = Inventory(component_id=created.id, state="on-hand-ready", quantity=3)
    create_inventory(inv)
    # Lead time report
    lead_report = get_lead_time_report()
    assert any(e["component_id"] == created.id for e in lead_report)
    # Failure rate report
    fail_report = get_failure_rate_report(0.05)
    assert any(e["component_id"] == created.id for e in fail_report)
    # Allocation validation
    valid, available = validate_inventory_allocation(created.id, 2)
    assert valid and available >= 2
    valid, available = validate_inventory_allocation(created.id, 10)
    assert not valid
    # Cost history report
    cost_hist = get_cost_history_report(created.id)
    assert len(cost_hist) == 2
    # Clean up
    delete_component(created.id)
