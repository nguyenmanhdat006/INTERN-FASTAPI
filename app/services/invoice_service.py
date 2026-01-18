from sqlalchemy.orm import Session
from datetime import datetime
from app.repositories import InvoiceRepository, ProductRepository
from app.schemas import InvoiceCreate, InvoiceUpdate


class InvoiceService:
    
    def __init__(self, db: Session):
        self.invoice_repo = InvoiceRepository(db)
        self.product_repo = ProductRepository(db)
        self.db = db
    
    def get_all_invoices(self, skip: int = 0, limit: int = 10):
        return self.invoice_repo.get_all(skip, limit)
    
    def get_invoice(self, invoice_id: int):
        return self.invoice_repo.get_by_id(invoice_id)
    
    def create_invoice(self, invoice: InvoiceCreate):
        invoice_number = f"INV-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        total_amount = 0
        for item in invoice.items:
            total_amount += item.unit_price * item.quantity
        
        invoice_data = {
            "invoice_number": invoice_number,
            "customer_name": invoice.customer_name,
            "total_amount": total_amount,
            "notes": invoice.notes,
        }
        
        db_invoice = self.invoice_repo.create(invoice_data)
        
        for item in invoice.items:
            item_data = {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "total_price": item.unit_price * item.quantity,
            }
            self.invoice_repo.add_item(db_invoice.id, item_data)
            
            product = self.product_repo.get_by_id(item.product_id)
            if product:
                product.quantity_in_stock -= item.quantity
                self.db.commit()
        
        self.db.refresh(db_invoice)
        return db_invoice
    
    def update_invoice(self, invoice_id: int, invoice: InvoiceUpdate):
        invoice_data = invoice.model_dump(exclude_unset=True)
        return self.invoice_repo.update(invoice_id, invoice_data)
    
    def delete_invoice(self, invoice_id: int):
        invoice = self.invoice_repo.get_by_id(invoice_id)
        if invoice:
            for item in invoice.items:
                product = self.product_repo.get_by_id(item.product_id)
                if product:
                    product.quantity_in_stock += item.quantity
                    self.db.commit()
        
        return self.invoice_repo.delete(invoice_id)
