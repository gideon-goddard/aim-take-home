from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator

# Models
def get_models():
    class Cost(BaseModel):
        value: float
        date: datetime

    class Component(BaseModel):
        id: Optional[str] = None
        component_id: Optional[int] = None
        vendor_name: str
        manufacturer_name: str
        estimated_lead_time: Optional[str] = None
        actual_lead_time: Optional[int] = 0
        order_link: Optional[str] = None
        failure_rate: Optional[float] = 0.0
        vendor_owner: Optional[str] = None
        model: Optional[str] = None
        pre_setup_required: Optional[bool] = False
        name: Optional[str] = None
        notes: Optional[str] = None
        costs: Optional[List[Cost]] = Field(default_factory=list)
        cost: Optional[float] = None

        @validator('failure_rate')
        def failure_rate_non_negative(cls, v):
            if v is not None and v < 0:
                raise ValueError('Failure rate must be non-negative')
            return v

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
        component_id: str
        state: str
        quantity: int = 1
        state_history: List[Dict[str, Any]] = Field(default_factory=list)
        serial_number: Optional[str] = None
        kit_id: Optional[str] = None
        sub_items: List[str] = Field(default_factory=list)

        @validator('quantity')
        def quantity_positive(cls, v):
            if v < 1:
                raise ValueError('Quantity must be at least 1')
            return v

    class HardwareRevision(BaseModel):
        id: Optional[str] = None
        name: str
        components: List[Dict[str, Any]] = Field(default_factory=list)

    return Cost, Component, InventoryState, Inventory, HardwareRevision

Cost, Component, InventoryState, Inventory, HardwareRevision = get_models()
