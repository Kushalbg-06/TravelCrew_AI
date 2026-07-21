"""
Central place for all environment-driven configuration.
Everything else in the project imports from here instead of
calling os.getenv() directly.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # LLM
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini/gemini-1.5-flash")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # Tools
    SERPER_API_KEY: str = os.getenv("SERPER_API_KEY", "")
    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY", "")
    GOOGLE_MAPS_API_KEY: str = os.getenv("GOOGLE_MAPS_API_KEY", "")

    # Database
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "trip_planner")

    @classmethod
    def validate(cls) -> list[str]:
        """Return a list of human-readable warnings for missing config."""
        warnings = []
        if "gemini" in cls.LLM_MODEL and not cls.GEMINI_API_KEY:
            warnings.append("GEMINI_API_KEY is not set but LLM_MODEL uses Gemini.")
        if "openai" in cls.LLM_MODEL and not cls.OPENAI_API_KEY:
            warnings.append("OPENAI_API_KEY is not set but LLM_MODEL uses OpenAI.")
        if not cls.SERPER_API_KEY:
            warnings.append("SERPER_API_KEY is not set - destination research will be limited.")
        if not cls.WEATHER_API_KEY:
            warnings.append("WEATHER_API_KEY is not set - weather lookups will be skipped.")
        return warnings


settings = Settings()
