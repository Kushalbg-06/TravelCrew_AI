"""
AI Personal Travel Planner - CLI entry point.

    python main.py
"""
from config.settings import settings
from database.mongodb import MongoDB
from memory.preferences import get_or_create_user, update_preferences, get_preferences
from memory.trip_history import save_trip, get_trips_for_user
from memory.conversation import log_turn, remember, recall
from database.models import Trip, Itinerary
from crews.travel_crew import run_travel_crew
from utils.formatter import (
    banner, ask, ask_choice, confirm, info, success, warn, show_plan, console,
)

TRANSPORT_OPTIONS = {"1": "Flight", "2": "Train", "3": "Bus"}
HOTEL_OPTIONS = {"1": "Budget", "2": "Premium", "3": "Luxury"}
INTEREST_OPTIONS = {
    "1": "Beaches", "2": "Nature", "3": "Adventure",
    "4": "Shopping", "5": "Photography",
}


def welcome(user_name: str, email: str) -> None:
    banner("AI Personal Travel Planner")
    trips = get_trips_for_user(email)
    prefs = get_preferences(email)
    memories = recall(email, limit=5)

    if trips or memories:
        console.print(f"\n[bold]Welcome back {user_name}![/bold]\n")
        if prefs.hotel_tier:
            success(f"{prefs.hotel_tier} Hotels")
        if prefs.food_preference:
            success(prefs.food_preference)
        if prefs.interests:
            success(", ".join(prefs.interests))
        if trips:
            console.print("\n[bold]Previous Trips[/bold]")
            for t in trips[:5]:
                console.print(f"  • {t.destination}")
    else:
        console.print(f"\n[bold]Welcome {user_name}![/bold] Let's plan your first trip.\n")


def collect_trip_requirements(source_default: str = "") -> dict:
    console.print()
    source = ask(f"Where are you travelling from? [{source_default}]") or source_default
    destination = ask("Destination?")
    budget = float(ask("Budget (₹)?"))
    days = int(ask("Number of days?"))
    travellers = int(ask("Number of travellers?"))

    console.print("\nPreferred transport?\n  1. Flight\n  2. Train\n  3. Bus")
    transport = TRANSPORT_OPTIONS[ask_choice("Choose", list(TRANSPORT_OPTIONS.keys()))]

    console.print("\nHotel preference?\n  1. Budget\n  2. Premium\n  3. Luxury")
    hotel_pref = HOTEL_OPTIONS[ask_choice("Choose", list(HOTEL_OPTIONS.keys()))]

    food_pref = ask("Food Preference?")

    console.print(
        "\nInterests?\n  1. Beaches\n  2. Nature\n  3. Adventure\n"
        "  4. Shopping\n  5. Photography"
    )
    raw = ask("Choose (space-separated numbers, e.g. 1 3 5)")
    interests = [INTEREST_OPTIONS[n] for n in raw.split() if n in INTEREST_OPTIONS]

    return {
        "source": source,
        "destination": destination,
        "budget": budget,
        "days": days,
        "travellers": travellers,
        "transport_pref": transport,
        "hotel_pref": hotel_pref,
        "food_pref": food_pref,
        "interests": interests,
    }


def plan_new_trip(user_name: str, email: str) -> None:
    prefs = get_preferences(email)
    trip_input = collect_trip_requirements()

    remembered = "; ".join(m.text for m in recall(email, limit=5))

    console.print("\n[bold]Starting Crew...[/bold]")
    plan_text = run_travel_crew(trip_input, remembered)
    show_plan(plan_text)

    log_turn(email, f"Plan a trip to {trip_input['destination']}", plan_text)

    if confirm("\nWould you like to save this trip?"):
        info("Saving...")
        trip = Trip(
            user_email=email,
            source=trip_input["source"],
            destination=trip_input["destination"],
            budget=trip_input["budget"],
            days=trip_input["days"],
            travellers=trip_input["travellers"],
            transport=trip_input["transport_pref"],
            hotel_preference=trip_input["hotel_pref"],
            food_preference=trip_input["food_pref"],
            interests=trip_input["interests"],
            itinerary=Itinerary(raw_plan=plan_text),
        )
        save_trip(trip)
        success("Trip Saved")

        update_preferences(
            email,
            hotel_tier=trip_input["hotel_pref"],
            food_preference=trip_input["food_pref"],
            interests=trip_input["interests"],
            preferred_transport=trip_input["transport_pref"],
        )
        success("User Preferences Updated")

        remember(email, f"User prefers {trip_input['hotel_pref']} hotels.", importance="high")
        remember(email, f"User food preference: {trip_input['food_pref']}.", importance="medium")
        success("Memory Updated")


def view_previous_trips(email: str) -> None:
    trips = get_trips_for_user(email)
    if not trips:
        warn("No previous trips found.")
        return
    banner("Travel History")
    for t in trips:
        console.print(f"  • {t.destination}  |  {t.days} days  |  ₹{t.budget:,.0f}")


def update_preferences_flow(email: str) -> None:
    console.print("\nUpdate which preference?")
    hotel_pref = ask("Hotel tier (Budget/Premium/Luxury) [leave blank to skip]")
    food_pref = ask("Food preference [leave blank to skip]")
    update_preferences(
        email,
        hotel_tier=hotel_pref or None,
        food_preference=food_pref or None,
    )
    success("Preferences updated")


def main() -> None:
    warnings = settings.validate()
    for w in warnings:
        warn(w)

    if not MongoDB.ping():
        warn("Could not reach MongoDB - check MONGODB_URI in .env. Continuing anyway.")

    console.print()
    user_name = ask("What's your name?")
    email = ask("What's your email?")
    get_or_create_user(user_name, email)

    while True:
        welcome(user_name, email)
        console.print(
            "\nWhat would you like to do?\n"
            "  1. Plan New Trip\n"
            "  2. View Previous Trips\n"
            "  3. Update Preferences\n"
            "  4. Exit\n"
        )
        choice = ask_choice("Enter your choice", ["1", "2", "3", "4"])

        if choice == "1":
            plan_new_trip(user_name, email)
        elif choice == "2":
            view_previous_trips(email)
        elif choice == "3":
            update_preferences_flow(email)
        elif choice == "4":
            console.print("\n[bold cyan]Have a safe journey! Goodbye.[/bold cyan]")
            break


if __name__ == "__main__":
    main()
