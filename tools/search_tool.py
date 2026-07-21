"""
Thin wrapper factory around crewai_tools' SerperDevTool so the rest
of the app never has to think about whether the API key is present.
"""
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from config.settings import settings


class SearchToolInput(BaseModel):
    query: str = Field(..., description="Search query, e.g. 'best beaches in Goa'")


class DestinationSearchTool(BaseTool):
    name: str = "Destination Web Search"
    description: str = (
        "Searches the web for up-to-date information about a destination: "
        "attractions, safety, best time to visit, local tips."
    )
    args_schema: type[BaseModel] = SearchToolInput

    def _run(self, query: str) -> str:
        if not settings.SERPER_API_KEY:
            return f"Search unavailable (no SERPER_API_KEY configured) for query: {query}"
        try:
            from crewai_tools import SerperDevTool
            tool = SerperDevTool()
            return tool.run(search_query=query)
        except Exception as e:
            return f"Search failed for '{query}': {e}"
