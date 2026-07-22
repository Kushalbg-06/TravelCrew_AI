"""
Reads/writes the User document (profile + preferences).
"""
from datetime import datetime
from database.mongodb import MongoDB
from database.models import User, UserPreferences


def get_or_create_user(name: str, email: str) -> User:
    doc = MongoDB.users().find_one({"email": email})
    if doc:
        doc.pop("_id", None)
        return User(**doc)

    user = User(name=name, email=email)
    MongoDB.users().insert_one(user.model_dump())
    return user


def update_preferences(email: str, **fields) -> None:
    """fields can include hotel_tier, food_preference, interests, preferred_transport"""
    updates = {f"preferences.{k}": v for k, v in fields.items() if v is not None}
    if not updates:
        return
    MongoDB.users().update_one({"email": email}, {"$set": updates}, upsert=True)


def get_preferences(email: str) -> UserPreferences:
    doc = MongoDB.users().find_one({"email": email}) or {}
    return UserPreferences(**doc.get("preferences", {}))
