"""
Pydantic models mirroring the MongoDB documents described in the
project spec: User, Trip, ConversationEntry, MemoryItem.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class UserPreferences(BaseModel):
    hotel_tier: Optional[str] = None          # Budget / Premium / Luxury
    food_preference: Optional[str] = None      # Vegetarian / Non-Vegetarian / ...
    interests: list[str] = Field(default_factory=list)
    preferred_transport: Optional[str] = None


class User(BaseModel):
    name: str
    email: str
    preferences: UserPreferences = Field(default_factory=UserPreferences)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Itinerary(BaseModel):
    hotel: Optional[str] = None
    activities: list[str] = Field(default_factory=list)
    restaurant: Optional[str] = None
    weather_summary: Optional[str] = None
    raw_plan: Optional[str] = None  # full text output from the crew


class Trip(BaseModel):
    user_email: str
    source: str
    destination: str
    budget: float
    days: int
    travellers: int
    transport: str
    hotel_preference: str
    food_preference: str
    interests: list[str] = Field(default_factory=list)
    itinerary: Optional[Itinerary] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ConversationEntry(BaseModel):
    user_email: str
    user_message: str
    assistant_reply: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class MemoryItem(BaseModel):
    user_email: str
    text: str                  # e.g. "User prefers budget hotels."
    importance: str = "medium"  # low / medium / high
    created_at: datetime = Field(default_factory=datetime.utcnow)
