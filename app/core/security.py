from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client, Client
from app.core.config import settings

security = HTTPBearer()

# Singleton: created once per serverless instance, reused across requests
_auth_client: Client | None = None


def get_supabase_client() -> Client:
    global _auth_client
    if _auth_client is None:
        _auth_client = create_client(
            settings.PUBLIC_SUPABASE_URL,
            settings.PUBLIC_SUPABASE_ANON_KEY,
        )
    return _auth_client

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    token = credentials.credentials
    client = get_supabase_client()
    
    try:
        # Verify token with Supabase Auth
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
        
    # Return user id (which corresponds to patient_id in our schema)
    return response.user.id
