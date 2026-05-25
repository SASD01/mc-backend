from supabase import create_client, Client
from app.core.config import settings

# Singleton: se crea una sola vez por instancia serverless
_supabase_client: Client | None = None


def get_supabase() -> Client:
    """Return a cached Supabase client (service-role key for DB operations)."""
    global _supabase_client
    if _supabase_client is None:
        _supabase_client = create_client(
            settings.PUBLIC_SUPABASE_URL,
            settings.SUPABASE_SERVICE_ROLE_KEY,
        )
    return _supabase_client
