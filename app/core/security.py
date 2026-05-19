from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client, Client
from app.core.config import settings

security = HTTPBearer()

def get_supabase_client() -> Client:
    # Use anon key to validate user tokens via Supabase Auth
    return create_client(settings.PUBLIC_SUPABASE_URL, settings.PUBLIC_SUPABASE_ANON_KEY)

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
