"""
Reads/writes Trip documents.
"""
from database.mongodb import MongoDB
from database.models import Trip


def save_trip(trip: Trip) -> str:
    result = MongoDB.trips().insert_one(trip.model_dump())
    return str(result.inserted_id)


def get_trips_for_user(email: str) -> list[Trip]:
    docs = MongoDB.trips().find({"user_email": email}).sort("created_at", -1)
    trips = []
    for doc in docs:
        doc.pop("_id", None)
        trips.append(Trip(**doc))
    return trips


def get_destination_history(email: str) -> list[str]:
    return [t.destination for t in get_trips_for_user(email)]
