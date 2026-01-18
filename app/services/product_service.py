from sqlalchemy.orm import Session
from app.repositories import ProductRepository
from app.schemas import ProductCreate, ProductUpdate


class ProductService:
    
    def __init__(self, db: Session):
        self.repository = ProductRepository(db)
    
    def get_all_products(self, skip: int = 0, limit: int = 10, category_id: int = None):
        return self.repository.get_all(skip, limit, category_id)
    
    def get_product(self, product_id: int):
        return self.repository.get_by_id(product_id)
    
    def create_product(self, product: ProductCreate):
        product_data = product.model_dump()
        return self.repository.create(product_data)
    
    def update_product(self, product_id: int, product: ProductUpdate):
        product_data = product.model_dump(exclude_unset=True)
        return self.repository.update(product_id, product_data)
    
    def delete_product(self, product_id: int):
        return self.repository.delete(product_id)
    
    def update_stock(self, product_id: int, quantity: int):
        product = self.repository.get_by_id(product_id)
        if product:
            product.quantity_in_stock += quantity
            self.repository.db.commit()
            self.repository.db.refresh(product)
        return product
