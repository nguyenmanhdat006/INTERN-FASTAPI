import httpx
from fastapi import HTTPException
from app.core.config import get_settings

class KeycloakClient:
    def __init__(self):
        settings = get_settings()
        self.base_url = settings.KEYCLOAK_URL
        self.realm = settings.KEYCLOAK_REALM
        self.client_id = settings.KEYCLOAK_CLIENT_ID
        self.client_secret = settings.KEYCLOAK_CLIENT_SECRET

    async def get_admin_token(self) -> str:
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/realms/master/protocol/openid-connect/token",
                data=data
            )

        if resp.status_code != 200:
            raise HTTPException(500, "Cannot get admin token")

        return resp.json()["access_token"]

    async def create_user(self, token: str, user):
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        payload = {
            "username": user.username,
            "email": user.email,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "enabled": True,
            "attributes": {
                "dob": user.dob.isoformat()
            },
            "credentials": [
                {
                    "type": "password",
                    "value": user.password,
                    "temporary": False
                }
            ]
        }

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/admin/realms/{self.realm}/users",
                headers=headers,
                json=payload
            )

        if resp.status_code != 201:
            raise HTTPException(
                status_code=400,
                detail=f"Create user in Keycloak failed: {resp.text}"
            )

        location = resp.headers.get("Location")
        if not location:
            raise HTTPException(500, "Missing Location header")

        return location.split("/")[-1]
