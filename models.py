from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator

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

        @field_validator('vendor_name', 'manufacturer_name', 'model', 'name', mode='before')
        def not_empty_string(cls, v, info):
            if v is not None and isinstance(v, str) and not v.strip():
                raise ValueError(f'{info.field_name} cannot be empty')
            return v

        @field_validator('actual_lead_time')
        def lead_time_non_negative(cls, v):
            if v is not None and v < 0:
                raise ValueError('actual_lead_time must be non-negative')
            return v

        @field_validator('failure_rate')
        def failure_rate_non_negative(cls, v):
            if v is not None and v < 0:
                raise ValueError('Failure rate must be non-negative')
            return v

        @field_validator('order_link')
        def valid_url(cls, v):
            if v is not None and v.strip() and not (v.startswith('http://') or v.startswith('https://')):
                raise ValueError('order_link must be a valid URL')
            return v

        @field_validator('cost')
        def cost_non_negative(cls, v):
            if v is not None and v < 0:
                raise ValueError('cost must be non-negative')
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

        @field_validator('component_id')
        def component_id_not_empty(cls, v):
            if not v or not v.strip():
                raise ValueError('component_id cannot be empty')
            return v

        @field_validator('quantity')
        def quantity_positive(cls, v):
            if v < 1:
                raise ValueError('Quantity must be at least 1')
            return v

        @field_validator('state')
        def valid_state(cls, v):
            valid_states = [
                "ordered", "received", "setup", "on-hand-ready",
                "allocated", "in-production", "failed"
            ]
            if v not in valid_states:
                raise ValueError(f'state must be one of {valid_states}')
            return v

        @field_validator('serial_number', 'kit_id', mode='before')
        def not_empty_optional_str(cls, v, info):
            if v is not None and not v.strip():
                raise ValueError(f'{info.field_name} cannot be empty if provided')
            return v

    class HardwareRevision(BaseModel):
        id: Optional[str] = None
        name: str
        components: List[Dict[str, Any]] = Field(default_factory=list)

        @field_validator('name', mode='before')
        def name_not_empty(cls, v, info):
            if not v or not v.strip():
                raise ValueError('name cannot be empty')
            return v

    return Cost, Component, InventoryState, Inventory, HardwareRevision

Cost, Component, InventoryState, Inventory, HardwareRevision = get_models()
