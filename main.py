import sys
import time
from models import Component, Inventory, HardwareRevision
from operations import (
    create_component, get_component, update_component, delete_component,
    create_inventory, get_inventory, update_inventory, delete_inventory,
    create_hardware_revision, get_hardware_revision, update_hardware_revision, delete_hardware_revision,
    update_component_cost, get_component_cost_history
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
        elif choice == "0":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid option.")

def demo_cli():
    print("\n--- CLI Automated Demo ---")
    time.sleep(0.5)
    # 1. Add a component
    comp = Component(vendor_name="DemoVendor", manufacturer_name="DemoManu")
    created = create_component(comp)
    print(f"Added component: {created}")
    time.sleep(0.5)
    # 2. Update component cost
    updated = update_component_cost(created.id, 123.45)
    print(f"Updated component cost: {updated.cost}")
    time.sleep(0.5)
    # 3. Add inventory
    inv = Inventory(component_id=created.id, state="ordered", quantity=2)
    items = create_inventory(inv)
    print(f"Added inventory: {[item.id for item in items]}")
    time.sleep(0.5)
    # 4. Update inventory state
    for item in items:
        updated_inv = update_inventory(item.id, {"state": "received"})
        print(f"Updated inventory {item.id} state to: {updated_inv.state}")
        time.sleep(0.5)
    # 5. Add hardware revision
    hw = HardwareRevision(name="DemoRev")
    created_hw = create_hardware_revision(hw)
    print(f"Added hardware revision: {created_hw}")
    time.sleep(0.5)
    # 6. Show cost history
    update_component_cost(created.id, 200.00)
    history = get_component_cost_history(created.id)
    print("Component cost history:")
    for cost in history:
        print(f"  Value: {cost.value}, Date: {cost.date}")
        time.sleep(0.3)
    print("--- End of CLI Automated Demo ---\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo_cli()
    else:
        main_menu()
