"""
All CrewAI Task definitions.

This crew runs under Process.hierarchical, so tasks intentionally do
NOT set `agent=`. The manager agent (crews/manager_agent.py) reads
each task's description and decides which specialist in the crew's
agents=[...] list should execute it. `context=` still expresses the
data dependencies between tasks, exactly as it would in sequential
mode.
"""
from crewai import Task


def build_tasks(trip_input: dict, remembered_preferences: str) -> list[Task]:
    """
    trip_input keys: source, destination, budget, days, travellers,
                      transport_pref, hotel_pref, food_pref, interests (list)
    Returns the ordered task list to hand to the Crew.
    """

    t_profile = Task(
        description=(
            f"Build a traveller brief from this input: {trip_input}. "
            f"Also factor in these remembered preferences: {remembered_preferences or 'none yet'}. "
            "Summarize constraints (budget, days, travellers, transport/hotel/food "
            "preference, interests) clearly for other agents. "
            "This belongs to the User Profile Analyst."
        ),
        expected_output="A short bullet-point traveller brief.",
    )

    t_research = Task(
        description=(
            f"Research {trip_input['destination']} focusing on these interests: "
            f"{trip_input['interests']}. Find 3-5 relevant attractions or experiences. "
            "This belongs to the Destination Research Specialist."
        ),
        expected_output="A short list of destination highlights matching the interests.",
        context=[t_profile],
    )

    t_weather = Task(
        description=(
            f"Check the current weather in {trip_input['destination']} and "
            "note any packing or timing implications. This belongs to the "
            "Weather Analyst."
        ),
        expected_output="A 1-2 sentence weather summary with practical advice.",
        context=[t_profile],
    )

    t_transport = Task(
        description=(
            f"Recommend the best {trip_input['transport_pref']} option from "
            f"{trip_input['source']} to {trip_input['destination']} for "
            f"{trip_input['travellers']} traveller(s), within the overall budget "
            f"of {trip_input['budget']}. This belongs to the Transport Planner."
        ),
        expected_output="A transport recommendation with an estimated cost.",
        context=[t_profile],
    )

    t_budget = Task(
        description=(
            f"Given a total budget of {trip_input['budget']} for "
            f"{trip_input['days']} days and {trip_input['travellers']} traveller(s), "
            "allocate it across transport, hotel, food, and activities. Use the "
            "transport recommendation already produced. This belongs to the "
            "Budget Planner."
        ),
        expected_output="A budget breakdown by category that sums to at most the total budget.",
        context=[t_profile, t_transport],
    )

    t_hotel = Task(
        description=(
            f"Recommend a {trip_input['hotel_pref']}-tier hotel in "
            f"{trip_input['destination']} that fits inside the hotel portion of the "
            "budget. This belongs to the Hotel Recommendation Specialist."
        ),
        expected_output="A hotel name with a one-line reason it fits.",
        context=[t_budget, t_research],
    )

    t_restaurant = Task(
        description=(
            f"Recommend a restaurant in {trip_input['destination']} matching "
            f"the food preference: {trip_input['food_pref']}. This belongs to "
            "the Restaurant Recommendation Specialist."
        ),
        expected_output="A restaurant name with a one-line reason it fits.",
        context=[t_research],
    )

    t_activities = Task(
        description=(
            f"Build a day-by-day activity list for {trip_input['days']} days in "
            f"{trip_input['destination']}, matching interests: {trip_input['interests']}. "
            "This belongs to the Activity Planner."
        ),
        expected_output="A day-by-day list of activities.",
        context=[t_research, t_weather],
    )

    t_itinerary = Task(
        description=(
            "Combine the transport, hotel, restaurant, weather, and activity "
            "recommendations into one coherent day-by-day itinerary. This "
            "belongs to the Itinerary Planner."
        ),
        expected_output="A structured day-by-day itinerary.",
        context=[t_transport, t_hotel, t_restaurant, t_weather, t_activities],
    )

    t_final = Task(
        description=(
            "Review the full itinerary against the total budget and traveller "
            "brief. This belongs to the Travel Advisor. Produce the final travel "
            "plan in this exact format:\n\n"
            "Destination: <name>\n"
            "Weather: <short summary>\n"
            "Budget: <total estimated cost>\n"
            "Hotel: <name>\n"
            "Activities: <comma-separated list>\n"
            "Restaurant: <name>\n"
            "Trip Duration: <N Days>\n"
        ),
        expected_output="The final formatted travel plan.",
        context=[t_itinerary, t_budget],
    )

    return [
        t_profile, t_research, t_weather, t_transport, t_budget,
        t_hotel, t_restaurant, t_activities, t_itinerary, t_final,
    ]
