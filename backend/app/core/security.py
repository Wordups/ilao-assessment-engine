from dataclasses import dataclass
from functools import lru_cache

import httpx
from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.core.config import Settings, get_settings


@dataclass
class CurrentUser:
    user_id: str
    email: str | None = None


class SupabaseTokenVerifier:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._jwks: dict | None = None

    async def _load_jwks(self) -> dict:
        if self._jwks is None:
            if not self.settings.supabase_jwks_url:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Supabase JWKS URL is not configured.",
                )
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(self.settings.supabase_jwks_url)
                response.raise_for_status()
                self._jwks = response.json()
        return self._jwks

    async def verify(self, token: str) -> CurrentUser:
        jwks = await self._load_jwks()
        try:
            header = jwt.get_unverified_header(token)
            key = next((item for item in jwks["keys"] if item["kid"] == header["kid"]), None)
            if key is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unknown signing key.")
            claims = jwt.decode(
                token,
                key,
                algorithms=[header["alg"]],
                audience=self.settings.supabase_audience,
                issuer=self.settings.supabase_issuer,
                options={"verify_aud": self.settings.supabase_audience is not None},
            )
        except (JWTError, KeyError, httpx.HTTPError) as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token.",
            ) from exc
        return CurrentUser(user_id=claims["sub"], email=claims.get("email"))


security_scheme = HTTPBearer(auto_error=False)


@lru_cache
def get_token_verifier() -> SupabaseTokenVerifier:
    return SupabaseTokenVerifier(get_settings())


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security_scheme),
    x_dev_user: str | None = Header(default=None),
    settings: Settings = Depends(get_settings),
    verifier: SupabaseTokenVerifier = Depends(get_token_verifier),
) -> CurrentUser:
    if settings.auth_mode == "development":
        return CurrentUser(user_id=x_dev_user or settings.dev_user_id, email=settings.dev_user_email)

    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token.")

    return await verifier.verify(credentials.credentials)
