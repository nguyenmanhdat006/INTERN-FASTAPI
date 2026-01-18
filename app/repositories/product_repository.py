from sqlalchemy.orm import Session
from app.models import Product


class ProductRepository:
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 10, category_id: int = None):
        query = self.db.query(Product)
        if category_id:
            query = query.filter(Product.category_id == category_id)
        return query.offset(skip).limit(limit).all()
    
    def get_by_id(self, product_id: int):
        return self.db.query(Product).filter(Product.id == product_id).first()
    
    def get_by_name(self, name: str):
        return self.db.query(Product).filter(Product.name == name).first()
    
    def create(self, product_data: dict):
        db_product = Product(**product_data)
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product
    
    def update(self, product_id: int, product_data: dict):
        db_product = self.get_by_id(product_id)
        if db_product:
            for key, value in product_data.items():
                if value is not None:
                    setattr(db_product, key, value)
            self.db.commit()
            self.db.refresh(db_product)
        return db_product
    
    def delete(self, product_id: int):
        db_product = self.get_by_id(product_id)
        if db_product:
            self.db.delete(db_product)
            self.db.commit()
        return db_product
