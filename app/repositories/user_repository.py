from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_username(self, username: str) -> User:
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, user_id: int) -> User:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_keycloak_id(self, keycloak_id: str) -> User:
        return self.db.query(User).filter(User.keycloak_id == keycloak_id).first()

    def create_user_with_keycloak(self, *, keycloak_id, user_data):
        user = User(
            keycloak_id=keycloak_id,
            username=user_data.username,
            email=user_data.email,
            first_name=user_data.firstName,
            last_name=user_data.lastName,
            dob=user_data.dob
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
