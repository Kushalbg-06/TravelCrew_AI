"""
Reads/writes conversation log entries and free-text "memory items"
(the ones with an importance level, e.g. "User prefers budget hotels.").
"""
from database.mongodb import MongoDB
from database.models import ConversationEntry, MemoryItem


def log_turn(email: str, user_message: str, assistant_reply: str) -> None:
    entry = ConversationEntry(
        user_email=email,
        user_message=user_message,
        assistant_reply=assistant_reply,
    )
    MongoDB.conversations().insert_one(entry.model_dump())


def remember(email: str, text: str, importance: str = "medium") -> None:
    item = MemoryItem(user_email=email, text=text, importance=importance)
    MongoDB.memories().insert_one(item.model_dump())


def recall(email: str, limit: int = 10) -> list[MemoryItem]:
    docs = (
        MongoDB.memories()
        .find({"user_email": email})
        .sort("created_at", -1)
        .limit(limit)
    )
    items = []
    for doc in docs:
        doc.pop("_id", None)
        items.append(MemoryItem(**doc))
    return items
