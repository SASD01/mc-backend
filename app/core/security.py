from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client, Client
from app.core.config import settings

security = HTTPBearer()

# Singleton: se crea una sola vez por instancia serverless
_auth_client: Client | None = None


def _get_auth_client() -> Client:
    """Return a cached Supabase client (anon key for auth verification)."""
    global _auth_client
    if _auth_client is None:
        _auth_client = create_client(
            settings.PUBLIC_SUPABASE_URL,
            settings.PUBLIC_SUPABASE_ANON_KEY,
        )
    return _auth_client


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    token = credentials.credentials
    client = _get_auth_client()

    try:
        response = client.auth.get_user(token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not response or not response.user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return response.user.id
