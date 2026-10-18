"""
Core configuration settings for the AI Sycophancy Lab application.
"""

from typing import List, Literal
from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path


# Get the path to the .env file in the backend directory
backend_dir = Path(__file__).parent.parent.parent
env_file_path = backend_dir / ".env"


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application settings
    app_name: str = Field(default="AI Sycophancy Lab")
    app_version: str = Field(default="1.0.0")
    debug: bool = Field(default=False)
    
    # API settings
    api_prefix: str = Field(default="/api")
    
    # CORS settings
    cors_origins: List[str] = Field(default=["http://localhost:3000", "http://127.0.0.1:3000"])
    
    # Database settings
    database_url: str = Field(default="sqlite+aiosqlite:///./data/sycophancy_lab.db")
    
    # LLM settings
    llm_provider: Literal["mock", "openai", "azure", "deepseek"] = Field(default="mock")
    openai_api_key: str = Field(default="")
    openai_model: str = Field(default="gpt-3.5-turbo")
    openai_temperature: float = Field(default=0.3)
    openai_max_tokens: int = Field(default=500)
    openai_timeout: int = Field(default=30)
    
    # DeepSeek settings
    deepseek_api_key: str = Field(default="")
    deepseek_model: str = Field(default="deepseek-chat")
    deepseek_temperature: float = Field(default=0.3)
    deepseek_max_tokens: int = Field(default=500)
    deepseek_timeout: int = Field(default=30)
    deepseek_base_url: str = Field(default="https://api.deepseek.com/v1")
    
    # Research settings
    study_id: str = Field(default="study4_pilot")
    experiment_mode: Literal["development", "approved_research"] = Field(default="development")
    
    # Logging settings
    store_message_text: bool = Field(default=True)
    redact_direct_identifiers: bool = Field(default=True)
    include_prompt_version: bool = Field(default=True)
    include_config_hash: bool = Field(default=True)
    
    class Config:
        env_file = str(env_file_path)
        env_file_encoding = "utf-8"
        case_sensitive = False


_settings = None


def get_settings() -> Settings:
    """Get cached settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reset_settings() -> None:
    """Reset settings cache (useful for testing)."""
    global _settings
    _settings = None
