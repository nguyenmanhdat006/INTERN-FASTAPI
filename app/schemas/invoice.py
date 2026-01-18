from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum


class InvoiceStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class InvoiceItemCreate(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)


class InvoiceItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float
    total_price: float
    
    class Config:
        from_attributes = True


class InvoiceBase(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=200)
    notes: Optional[str] = Field(None, max_length=1000)


class InvoiceCreate(InvoiceBase):
    items: List[InvoiceItemCreate] = Field(..., min_items=1)


class InvoiceUpdate(BaseModel):
    customer_name: Optional[str] = Field(None, min_length=1, max_length=200)
    status: Optional[InvoiceStatus] = None
    notes: Optional[str] = Field(None, max_length=1000)


class InvoiceResponse(InvoiceBase):
    id: int
    invoice_number: str
    total_amount: float
    status: InvoiceStatus
    items: List[InvoiceItemResponse]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
