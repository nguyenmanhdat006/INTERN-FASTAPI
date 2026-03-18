from app.infra.keycloak_client import KeycloakClient
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.keycloak = KeycloakClient()

    async def register_user(self, user_data: UserCreate) -> UserResponse:
        if self.user_repo.get_user_by_username(user_data.username):
            raise HTTPException(400, "Username already registered")

        if self.user_repo.get_user_by_email(user_data.email):
            raise HTTPException(400, "Email already registered")

        admin_token = await self.keycloak.get_admin_token()

        keycloak_user_id = await self.keycloak.create_user(
            admin_token, user_data
        )

        db_user = self.user_repo.create_user_with_keycloak(
            keycloak_id=keycloak_user_id,
            user_data=user_data
        )

        return UserResponse.from_orm(db_user)
