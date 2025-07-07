import sys
import time
from models import Component, Inventory, HardwareRevision
from operations import (
    create_component, get_component, update_component, delete_component,
    create_inventory, get_inventory, update_inventory, delete_inventory,
    create_hardware_revision, get_hardware_revision, update_hardware_revision, delete_hardware_revision,
    update_component_cost, get_component_cost_history,
    list_inventory, verify_hardware_revision_inventory,
    get_lead_time_report, get_failure_rate_report, validate_inventory_allocation, get_cost_history_report
)

def main_menu():
    while True:
        print("\nAIM Inventory Management CLI")
        print("1. Add Component")
        print("2. View Component")
        print("3. Update Component")
        print("4. Delete Component")
        print("5. Add Inventory")
        print("6. View Inventory")
        print("7. Update Inventory State")
        print("8. Delete Inventory")
        print("9. Add Hardware Revision")
        print("10. View Hardware Revision")
        print("11. Update Hardware Revision")
        print("12. Delete Hardware Revision")
        print("13. Update Component Cost")
        print("14. View Component Cost History")
        print("15. List All Inventory")
        print("16. Verify Hardware Revision Against Inventory")
        print("17. Lead Time Report")
        print("18. Failure Rate Analysis")
        print("19. Validate Inventory Allocation")
        print("20. Cost History Report")
        print("0. Exit")
        choice = input("Select an option: ")
        if choice == "1":
            vendor = input("Vendor name: ")
            manu = input("Manufacturer name: ")
            comp = Component(vendor_name=vendor, manufacturer_name=manu)
            created = create_component(comp)
            print(f"Created: {created}")
        elif choice == "2":
            cid = input("Component ID: ")
            comp = get_component(cid)
            print(comp or "Not found.")
        elif choice == "3":
            cid = input("Component ID: ")
            field = input("Field to update: ")
            value = input("New value: ")
            updated = update_component(cid, {field: value})
            print(updated or "Not found.")
        elif choice == "4":
            cid = input("Component ID: ")
            deleted = delete_component(cid)
            print("Deleted." if deleted else "Not found.")
        elif choice == "5":
            compid = input("Component ID: ")
            state = input("State: ")
            qty = int(input("Quantity: "))
            inv = Inventory(component_id=compid, state=state, quantity=qty)
            items = create_inventory(inv)
            print(f"Created: {items}")
        elif choice == "6":
            iid = input("Inventory ID: ")
            inv = get_inventory(iid)
            print(inv or "Not found.")
        elif choice == "7":
            iid = input("Inventory ID: ")
            state = input("New state: ")
            updated = update_inventory(iid, {"state": state})
            print(updated or "Not found.")
        elif choice == "8":
            iid = input("Inventory ID: ")
            deleted = delete_inventory(iid)
            print("Deleted." if deleted else "Not found.")
        elif choice == "9":
            name = input("Hardware Revision Name: ")
            hw = HardwareRevision(name=name)
            created = create_hardware_revision(hw)
            print(f"Created: {created}")
        elif choice == "10":
            hwid = input("Hardware Revision ID: ")
            hw = get_hardware_revision(hwid)
            print(hw or "Not found.")
        elif choice == "11":
            hwid = input("Hardware Revision ID: ")
            field = input("Field to update: ")
            value = input("New value: ")
            updated = update_hardware_revision(hwid, {field: value})
            print(updated or "Not found.")
        elif choice == "12":
            hwid = input("Hardware Revision ID: ")
            deleted = delete_hardware_revision(hwid)
            print("Deleted." if deleted else "Not found.")
        elif choice == "13":
            cid = input("Component ID: ")
            new_cost = float(input("New cost: "))
            updated = update_component_cost(cid, new_cost)
            print(updated or "Not found.")
        elif choice == "14":
            cid = input("Component ID: ")
            history = get_component_cost_history(cid)
            if history:
                for cost in history:
                    print(f"Value: {cost.value}, Date: {cost.date}")
            else:
                print("No cost history or component not found.")
        elif choice == "15":
            state = input("Filter by state (or leave blank): ")
            component_id = input("Filter by component_id (or leave blank): ")
            items = list_inventory(state=state or None, component_id=component_id or None)
            if items:
                for item in items:
                    print(item)
            else:
                print("No inventory found.")
        elif choice == "16":
            hwid = input("Hardware Revision ID: ")
            result = verify_hardware_revision_inventory(hwid)
            if result is None:
                print("Hardware revision not found.")
            elif not result:
                print("All required components are available in inventory.")
            else:
                print("Missing or insufficient components:")
                for miss in result:
                    print(miss)
        elif choice == "17":
            report = get_lead_time_report()
            for entry in report:
                print(entry)
        elif choice == "18":
            threshold = float(input("Failure rate threshold (e.g. 0.05): "))
            report = get_failure_rate_report(threshold)
            if report:
                for entry in report:
                    print(entry)
            else:
                print("No components above threshold.")
        elif choice == "19":
            cid = input("Component ID: ")
            qty = int(input("Requested quantity: "))
            valid, available = validate_inventory_allocation(cid, qty)
            if valid:
                print(f"Enough inventory available: {available}")
            else:
                print(f"Not enough inventory. Available: {available}")
        elif choice == "20":
            cid = input("Component ID: ")
            report = get_cost_history_report(cid)
            if report:
                for entry in report:
                    print(entry)
            else:
                print("No cost history found.")
        elif choice == "0":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid option.")

def demo_cli():
    print("\n--- CLI Automated Demo ---")
    time.sleep(0.5)
    # 1. Add components: CPU, RAM, SSD, Power Supply
    cpu = Component(vendor_name="Intel", manufacturer_name="Intel", name="CPU", cost=300, estimated_lead_time="5d", actual_lead_time=7, failure_rate=0.01)
    ram = Component(vendor_name="Corsair", manufacturer_name="Corsair", name="RAM", cost=100, estimated_lead_time="2d", actual_lead_time=3, failure_rate=0.005)
    ssd = Component(vendor_name="Samsung", manufacturer_name="Samsung", name="SSD", cost=150, estimated_lead_time="3d", actual_lead_time=3, failure_rate=0.002)
    psu = Component(vendor_name="EVGA", manufacturer_name="EVGA", name="Power Supply", cost=80, estimated_lead_time="4d", actual_lead_time=4, failure_rate=0.02)
    cpu = create_component(cpu)
    ram = create_component(ram)
    ssd = create_component(ssd)
    psu = create_component(psu)
    print(f"Added components: {cpu.name}, {ram.name}, {ssd.name}, {psu.name}")
    time.sleep(0.5)
    # 2. Add inventory
    cpu_inv = create_inventory(Inventory(component_id=cpu.id, state="on-hand-ready", quantity=10))
    ram_inv = create_inventory(Inventory(component_id=ram.id, state="on-hand-ready", quantity=20))
    ssd_inv = create_inventory(Inventory(component_id=ssd.id, state="allocated", quantity=5))
    psu_inv = create_inventory(Inventory(component_id=psu.id, state="failed", quantity=2))
    print(f"Added inventory: 10 CPUs, 20 RAM, 5 SSDs (allocated), 2 PSUs (failed)")
    time.sleep(0.5)
    # 3. Create hardware revision
    hw = HardwareRevision(name="Server v1", components=[
        {"component_id": cpu.id, "quantity": 2},
        {"component_id": ram.id, "quantity": 4},
        {"component_id": ssd.id, "quantity": 1},
        {"component_id": psu.id, "quantity": 1},
    ])
    hw = create_hardware_revision(hw)
    print(f"Created hardware revision: {hw.name}")
    time.sleep(0.5)
    # 4. Update CPU cost twice
    update_component_cost(cpu.id, 320)
    update_component_cost(cpu.id, 350)
    print("Updated CPU cost twice to demonstrate cost history.")
    time.sleep(0.5)
    # 5. Inventory and cost history reports
    print("\nInventory report:")
    for item in list_inventory():
        print(item)
        time.sleep(0.1)
    print("\nCPU cost history:")
    for cost in get_component_cost_history(cpu.id):
        print(f"  Value: {cost.value}, Date: {cost.date}")
        time.sleep(0.1)
    # 6. Verify hardware revision
    print(f"\nVerifying if '{hw.name}' can be built from current inventory:")
    result = verify_hardware_revision_inventory(hw.id)
    if not result:
        print("All required components are available in inventory.")
    else:
        print("Missing or insufficient components:")
        for miss in result:
            print(miss)
    time.sleep(0.5)
    # 7. Lead time report
    print("\nLead time report:")
    for entry in get_lead_time_report():
        print(entry)
        time.sleep(0.1)
    # 8. Failure rate analysis
    print("\nFailure rate analysis (threshold 0.0):")
    for entry in get_failure_rate_report(0.0):
        print(entry)
        time.sleep(0.1)
    # 9. Validate allocation for 'Server v1' (CPU example)
    print(f"\nValidate inventory allocation for '{hw.name}' (CPU, request 2):")
    valid, available = validate_inventory_allocation(cpu.id, 2)
    print(f"Valid: {valid}, Available: {available}")
    print("--- End of CLI Automated Demo ---\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo_cli()
    else:
        main_menu()
