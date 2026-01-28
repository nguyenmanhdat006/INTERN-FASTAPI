from http.client import HTTPException
from jose import jwt
import requests

KEYCLOAK_REALM = "nguyendat"
KEYCLOAK_URL = "http://localhost:8081"
ALGORITHM = "RS256"

jwks = requests.get(
    f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/certs"
).json()

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            jwks,
            algorithms=[ALGORITHM],
            audience="account",
            issuer=f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}",
        )
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
