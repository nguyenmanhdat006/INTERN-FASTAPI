from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
import httpx

from app.core.config import get_settings
from app.core.database import get_db
from app.repositories.user_repository import UserRepository

security = HTTPBearer()
ALGORITHM = "RS256"

_jwks_cache = None

async def get_jwks():
    global _jwks_cache
    settings = get_settings()

    if _jwks_cache is None:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/certs"
            )
            resp.raise_for_status()
            _jwks_cache = resp.json()
    return _jwks_cache


async def verify_token(token: str) -> dict:
    settings = get_settings()
    try:
        jwks = await get_jwks()
        payload = jwt.decode(
            token,
            jwks,
            algorithms=[ALGORITHM],
            issuer=f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}",
            options={"verify_aud": False},
        )
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db),
):
    token = credentials.credentials
    payload = await verify_token(token)

    keycloak_id = payload.get("sub")
    if not keycloak_id:
        raise HTTPException(401, "Invalid token payload")

    user = UserRepository(db).get_user_by_keycloak_id(keycloak_id)
    if not user:
        raise HTTPException(401, "User not found")

    user.roles = payload.get("realm_access", {}).get("roles", [])
    return user
