"""
Assembles the specialist agents + tasks into a Crew that runs under
Process.hierarchical.

How hierarchical differs from sequential:
- A manager_agent (crews/manager_agent.py) sits above all the
  specialists. It is NOT included in `agents=[...]`.
- The manager reads each Task, decides which specialist agent should
  execute it, delegates the work, and reviews the result before
  moving on - it can send a task back to the same or a different
  agent if the output doesn't hold up.
- Because the manager does the assigning, tasks in tasks/travel_tasks.py
  don't hardcode `agent=`; each task description simply names which
  specialist it "belongs to" as a strong hint to the manager.
"""
from crewai import Crew, Process

from agents import (
    user_profile_agent,
    destination_research_agent,
    weather_agent,
    budget_planner_agent,
    hotel_recommendation_agent,
    restaurant_recommendation_agent,
    transport_agent,
    activity_planner_agent,
    itinerary_planner_agent,
    travel_advisor_agent,
)
from crews.manager_agent import travel_manager_agent
from tasks.travel_tasks import build_tasks


def run_travel_crew(trip_input: dict, remembered_preferences: str = "") -> str:
    specialists = [
        user_profile_agent(),
        destination_research_agent(),
        weather_agent(),
        transport_agent(),
        budget_planner_agent(),
        hotel_recommendation_agent(),
        restaurant_recommendation_agent(),
        activity_planner_agent(),
        itinerary_planner_agent(),
        travel_advisor_agent(),
    ]

    tasks = build_tasks(trip_input, remembered_preferences)

    crew = Crew(
        agents=specialists,          # workers only - manager is separate
        tasks=tasks,
        process=Process.hierarchical,
        manager_agent=travel_manager_agent(),
        planning=False,              
        verbose=True,
    )

    result = crew.kickoff()
    return str(result)
