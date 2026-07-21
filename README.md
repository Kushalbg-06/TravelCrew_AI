# AI Personal Travel Planner (CrewAI, CLI-only)

A terminal-based multi-agent travel planner built with **CrewAI**, using
**MongoDB Atlas** for persistence (user profile, trip history, conversation
log, and long-term memory). No frontend, no backend server — just Python.

## Project Structure

```
trip_planner/
├── main.py                 # CLI entry point
├── config/
│   ├── settings.py         # env var loading
│   └── llm.py               # LLM factory (Gemini / OpenAI via LiteLLM)
├── agents/
│   └── travel_agents.py     # all 10 CrewAI Agent definitions
├── tasks/
│   └── travel_tasks.py      # all Task definitions + dependency wiring
├── crews/
│   └── travel_crew.py       # Crew assembly + kickoff
├── tools/
│   ├── weather_tool.py      # OpenWeatherMap
│   ├── search_tool.py       # Serper web search
│   └── maps_tool.py         # Google Maps distance (optional)
├── memory/
│   ├── conversation.py      # chat log + long-term memory items
│   ├── preferences.py       # user profile/preferences
│   └── trip_history.py      # saved trips
├── database/
│   ├── mongodb.py           # single Mongo client/collections
│   └── models.py            # Pydantic schemas
├── utils/
│   └── formatter.py         # rich-based CLI helpers
├── .env.example
├── requirements.txt
└── README.md
```

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# then fill in your API keys and MongoDB URI in .env
```

### Required keys

| Key | Where to get it |
|---|---|
| `GEMINI_API_KEY` or `OPENAI_API_KEY` | Google AI Studio / OpenAI dashboard |
| `SERPER_API_KEY` | serper.dev (free tier available) |
| `WEATHER_API_KEY` | openweathermap.org |
| `MONGODB_URI` | MongoDB Atlas connection string |
| `GOOGLE_MAPS_API_KEY` | optional, Google Cloud Console |

## Run

```bash
python main.py
```

You'll be asked for your name/email once (used as your profile key), then
dropped into the main menu:

```
1. Plan New Trip
2. View Previous Trips
3. Update Preferences
4. Exit
```

Planning a trip walks you through source, destination, budget, days,
travellers, transport, hotel tier, food preference, and interests, then
kicks off the crew:

```
Starting Crew...
✓ Research Agent
✓ Weather Agent
✓ Budget Agent
✓ Hotel Agent
✓ Restaurant Agent
✓ Activity Agent
✓ Advisor Agent
```

The final plan is shown, and — if you confirm — the trip, updated
preferences, and a couple of memory notes are saved to MongoDB so the next
run remembers you.

## How the agents fit together

```
User Profile Agent
        │
        ▼
Destination Research Agent ──► Weather Agent
        │                           │
        ▼                           │
Transport Agent ──► Budget Planner Agent
        │                           │
        ▼                           ▼
Hotel Agent      Restaurant Agent      Activity Planner Agent
        │               │                     │
        └───────────────┼─────────────────────┘
                         ▼
              Itinerary Planner Agent
                         │
                         ▼
                Travel Advisor Agent  (final output)
```

