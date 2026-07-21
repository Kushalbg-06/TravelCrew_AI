"""
Builds the LLM object handed to every agent.
CrewAI uses LiteLLM under the hood, so a plain model string
(e.g. "gemini/gemini-1.5-flash" or "openai/gpt-4o-mini") is enough -
LiteLLM picks up the matching *_API_KEY from the environment itself.
"""
import os
from crewai import LLM
from config.settings import settings

# Make sure the right env vars exist under the names LiteLLM expects
if settings.GEMINI_API_KEY:
    os.environ.setdefault("GEMINI_API_KEY", settings.GEMINI_API_KEY)
if settings.OPENAI_API_KEY:
    os.environ.setdefault("OPENAI_API_KEY", settings.OPENAI_API_KEY)


def get_llm(temperature: float = 0.4) -> LLM:
    return LLM(model=settings.LLM_MODEL, temperature=temperature)
