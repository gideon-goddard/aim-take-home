AIM Hardware Inventory Management System \- Take-Home Assignment 

Introduction 

AIM is a combined hardware/software company specializing in managing inventory from order to installation. As part of our interview process, we've prepared a take-home assignment to evaluate your problem-solving skills, coding abilities, and overall approach to software development. 

Background 

We have an existing inventory management system that tracks components, inventory items, and hardware revisions. Your task is to extend and improve upon this system. 

Assignment 

You will be provided with simplified versions of a few of our data models and basic operations. Your assignment consists of the following tasks: 

1\. **Fixing Issues in the Provided Models and Operations:** 
● Identify and correct any issues present in the given data models. 

● Implement appropriate validation where necessary. 

● Ensure consistency in naming conventions and data types. 

2\. **Implementing Core Functions:** 

● Complete the operations for basic CRUD (Create, Read, Update, Delete) functionality. 

● Add validation logic to prevent invalid operations. 

● Implement proper state tracking for inventory items. 

3\. **Building a User Interface:** 

● Build a solution that accomplishes the following: 

● Add, view, and update components 

● Manage inventory state transitions 

● Generate reports on current inventory 

● Verify hardware revisions against available inventory 

● Feel free to implement the solution in a way that works best for you 

4\. **Extending the System:** 

● Add at least **ONE** of the following features: 

● Component lead time tracking and reporting. 

● Failure rate tracking or analysis. 

● Inventory allocation validation. 

● Component cost history tracking.  
Solution Guidance: 

● You can edit/refactor any code or file/folder structure to achieve the task. ● Add testing to verify correctness and functionality 

Deliverables 

Please provide the following: 

● **Corrected and Extended Python Code:** Your modified Python code files. ● **User Interface Implementation:** Either your command-line interface or web interface. ● **Documentation:** A brief document explaining: 

● Issues you identified and fixed 

● Design decisions you made during your implementation 

● Instructions on how to run and use your solution. 

● Any assumptions you made. 

Evaluation Criteria 

Your submission will be evaluated based on the following: 

● **Attention to Detail:** Your ability to identify and fix issues. 

● **Code Quality and Organization:** The clarity, efficiency, and structure of your code. ● **User Interface Design and Usability:** The intuitiveness and effectiveness of your interface. ● **Documentation Quality:** The clarity and completeness of your documentation. ● **Testing Approach:** How you tested your solution. 

Time Estimate 

We estimate that this assignment should take no more than 3-5 hours to complete. We are looking for a working prototype that demonstrates your approach to the problem, not a production-ready system. 

We look forward to reviewing your submission\! 


```Python
from datetime import datetime 
from typing import List, Optional, Dict, Any, Union 
from pydantic import BaseModel, Field 

# Models
class Cost(BaseModel): 
    value: float 
    date: datetime 

class Component(BaseModel): 
    id: Optional[str] = None 
    componentId: Optional[int] = None vendorName: str 
    manufacturerName: str 
    estimatedLeadTime: str 
    actualLeadTime: int = 0 
    orderLink: str 
    failureRate: float = 0.0 
    vendorOwner: str 
    model: str 
    preSetupRequired: bool 
    name: Optional[str] = None 
    notes: Optional[str] = None 
    costs: Optional[List[Cost]] = [] 
    cost: Optional[float] = None 

class InventoryState(str): 
    ORDERED = "ordered" 
    RECEIVED = "received" 
    SETUP = "setup" 
    ON_HAND_READY = "on-hand-ready" 
    ALLOCATED = "allocated" 
    IN_PRODUCTION = "in-production" 
    FAILED = "failed" 

class Inventory(BaseModel): 
    id: Optional[str] = None 
    componentId: str 
    state: str 
    quantity: int = 1 
    stateHistory: List[Dict[str, Any]] = [] serialNumber: Optional[str] = None kitId: Optional[str] = None 
    subItems: List[str] = [] 

class HardwareRevision(BaseModel): id: Optional[str] = None 
    name: str 
    components: List[Dict[str, Any]] = []

# Operations (incomplete) 
async def get_next_component_id() -> str: 
    """Generate next component ID""" 
    return "COM-123" 

async def create_component(component: Component) -> Component: """Create a new component""" 
    return component 

async def create_inventory(inventory: Inventory) -> List[Inventory]: """Create inventory items""" 
    items = [] 
    for _ in range(inventory.quantity): 
        items.append(inventory) 
    return items 

async def update_inventory_state(inventory_id: str, state: str) -> Dict[str, str]: 
    """Update inventory state""" 
    return {"status": "success"} 

async def create_hardware_revision(hw_rev: HardwareRevision) -> HardwareRevision: 
    """Create a hardware revision""" 
    return hw_rev