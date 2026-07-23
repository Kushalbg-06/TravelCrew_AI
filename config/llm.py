"""
Creates a shared LLM instance for all CrewAI agents.

This project is provider-agnostic. The model is selected using the
LLM_MODEL environment variable, allowing you to switch providers
without changing any Python code.

Examples:

Gemini:
    LLM_MODEL=gemini/gemini-2.5-flash
    GEMINI_API_KEY=your_api_key

OpenAI:
    LLM_MODEL=openai/gpt-4o-mini
    OPENAI_API_KEY=your_api_key

OpenRouter:
    LLM_MODEL=openrouter/deepseek/deepseek-chat
    OPENROUTER_API_KEY=your_api_key
"""

import os

from crewai import LLM

from config.settings import settings


# Make API keys available for LiteLLM
if settings.GEMINI_API_KEY:
    os.environ.setdefault("GEMINI_API_KEY", settings.GEMINI_API_KEY)

if settings.OPENAI_API_KEY:
    os.environ.setdefault("OPENAI_API_KEY", settings.OPENAI_API_KEY)

if settings.OPENROUTER_API_KEY:
    os.environ.setdefault("OPENROUTER_API_KEY", settings.OPENROUTER_API_KEY)


def get_llm(temperature: float = 0.4) -> LLM:
    """
    Returns a configured LLM instance.

    LiteLLM automatically detects the provider from the model name
    and uses the corresponding API key from the environment.
    """

    return LLM(
        model=settings.LLM_MODEL,
        temperature=temperature,
    )