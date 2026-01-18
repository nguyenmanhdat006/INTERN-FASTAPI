from sqlalchemy.orm import Session
from app.models import Invoice, InvoiceItem


class InvoiceRepository:
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 10):
        return self.db.query(Invoice).offset(skip).limit(limit).all()
    
    def get_by_id(self, invoice_id: int):
        return self.db.query(Invoice).filter(Invoice.id == invoice_id).first()
    
    def get_by_number(self, invoice_number: str):
        return self.db.query(Invoice).filter(Invoice.invoice_number == invoice_number).first()
    
    def create(self, invoice_data: dict):
        db_invoice = Invoice(**invoice_data)
        self.db.add(db_invoice)
        self.db.commit()
        self.db.refresh(db_invoice)
        return db_invoice
    
    def update(self, invoice_id: int, invoice_data: dict):
        db_invoice = self.get_by_id(invoice_id)
        if db_invoice:
            for key, value in invoice_data.items():
                if value is not None:
                    setattr(db_invoice, key, value)
            self.db.commit()
            self.db.refresh(db_invoice)
        return db_invoice
    
    def delete(self, invoice_id: int):
        db_invoice = self.get_by_id(invoice_id)
        if db_invoice:
            self.db.delete(db_invoice)
            self.db.commit()
        return db_invoice
    
    def add_item(self, invoice_id: int, item_data: dict):
        db_item = InvoiceItem(invoice_id=invoice_id, **item_data)
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item
