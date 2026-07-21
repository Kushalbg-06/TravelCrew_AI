"""
Single shared MongoDB client + collection accessors.
Everything in memory/ goes through this module so there's only
one place that knows about pymongo.
"""
from pymongo import MongoClient
from pymongo.collection import Collection
from config.settings import settings


class MongoDB:
    _client: MongoClient | None = None

    @classmethod
    def client(cls) -> MongoClient:
        if cls._client is None:
            cls._client = MongoClient(settings.MONGODB_URI, serverSelectionTimeoutMS=5000)
        return cls._client

    @classmethod
    def db(cls):
        return cls.client()[settings.MONGODB_DB_NAME]

    @classmethod
    def users(cls) -> Collection:
        return cls.db()["users"]

    @classmethod
    def trips(cls) -> Collection:
        return cls.db()["trips"]

    @classmethod
    def conversations(cls) -> Collection:
        return cls.db()["conversations"]

    @classmethod
    def memories(cls) -> Collection:
        return cls.db()["memories"]

    @classmethod
    def ping(cls) -> bool:
        try:
            cls.client().admin.command("ping")
            return True
        except Exception:
            return False
