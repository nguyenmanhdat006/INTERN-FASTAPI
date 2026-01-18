from sqlalchemy.orm import Session
from app.models import Category


class CategoryRepository:
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 10):
        return self.db.query(Category).offset(skip).limit(limit).all()
    
    def get_by_id(self, category_id: int):
        return self.db.query(Category).filter(Category.id == category_id).first()
    
    def get_by_name(self, name: str):
        return self.db.query(Category).filter(Category.name == name).first()
    
    def create(self, category_data: dict):
        db_category = Category(**category_data)
        self.db.add(db_category)
        self.db.commit()
        self.db.refresh(db_category)
        return db_category
    
    def update(self, category_id: int, category_data: dict):
        db_category = self.get_by_id(category_id)
        if db_category:
            for key, value in category_data.items():
                if value is not None:
                    setattr(db_category, key, value)
            self.db.commit()
            self.db.refresh(db_category)
        return db_category
    
    def delete(self, category_id: int):
        db_category = self.get_by_id(category_id)
        if db_category:
            self.db.delete(db_category)
            self.db.commit()
        return db_category
