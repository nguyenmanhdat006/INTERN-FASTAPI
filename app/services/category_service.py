from sqlalchemy.orm import Session
from app.repositories import CategoryRepository
from app.schemas import CategoryCreate, CategoryUpdate


class CategoryService:
    
    def __init__(self, db: Session):
        self.repository = CategoryRepository(db)
    
    def get_all_categories(self, skip: int = 0, limit: int = 10):
        return self.repository.get_all(skip, limit)
    
    def get_category(self, category_id: int):
        return self.repository.get_by_id(category_id)
    
    def create_category(self, category: CategoryCreate):
        category_data = category.model_dump()
        return self.repository.create(category_data)
    
    def update_category(self, category_id: int, category: CategoryUpdate):
        category_data = category.model_dump(exclude_unset=True)
        return self.repository.update(category_id, category_data)
    
    def delete_category(self, category_id: int):
        return self.repository.delete(category_id)
