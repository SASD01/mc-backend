from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PUBLIC_SUPABASE_URL: str
    PUBLIC_SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_ROLE_KEY: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
