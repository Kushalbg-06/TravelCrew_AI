"""
Re-exports every agent factory so other modules can do:
    from agents import user_profile_agent, weather_agent, ...
"""
from agents.user_profile_agent import user_profile_agent
from agents.destination_research_agent import destination_research_agent
from agents.weather_agent import weather_agent
from agents.budget_planner_agent import budget_planner_agent
from agents.hotel_recommendation_agent import hotel_recommendation_agent
from agents.restaurant_recommendation_agent import restaurant_recommendation_agent
from agents.transport_agent import transport_agent
from agents.activity_planner_agent import activity_planner_agent
from agents.itinerary_planner_agent import itinerary_planner_agent
from agents.travel_advisor_agent import travel_advisor_agent

__all__ = [
    "user_profile_agent",
    "destination_research_agent",
    "weather_agent",
    "budget_planner_agent",
    "hotel_recommendation_agent",
    "restaurant_recommendation_agent",
    "transport_agent",
    "activity_planner_agent",
    "itinerary_planner_agent",
    "travel_advisor_agent",
]
