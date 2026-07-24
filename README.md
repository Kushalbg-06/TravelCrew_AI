# 🧳 AI Personal Travel Planner

A terminal-based, multi-agent travel planner built with **CrewAI**, using a
**hierarchical crew** (a manager agent delegating to 10 specialists) and
**MongoDB Atlas** for persistence — trip history, preferences, and long-term
memory across runs. CLI-only by design, so the agent/crew/memory logic stays
clean and reusable if a frontend gets added later.

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-blue)

---



## Features

- 🧭 **10 specialist agents** — profile, research, weather, transport, budget, hotel, restaurant, activities, itinerary, advisor
- 🧑‍💼 **Hierarchical delegation** — a manager agent assigns and reviews each task instead of a fixed sequential pipeline
- 🧠 **Persistent memory** — MongoDB-backed preferences, trip history, and conversation log; the CLI greets returning users with what it remembers
- 🔧 **Live tools** — real-time weather lookup, web search for destination research, and road-distance estimation
- 💻 **CLI-only** — no frontend/backend coupling; all planning logic lives behind a single `run_travel_crew()` call

---



## Project Structure

```
trip_planner/
├── main.py                        # CLI entry point
├── config/
│   ├── settings.py                # env var loading + validation
│   └── llm.py                     # LLM factory (Gemini / OpenAI via LiteLLM)
├── agents/                        # one file per specialist agent
│   ├── user_profile_agent.py
│   ├── destination_research_agent.py
│   ├── weather_agent.py
│   ├── transport_agent.py
│   ├── budget_planner_agent.py
│   ├── hotel_recommendation_agent.py
│   ├── restaurant_recommendation_agent.py
│   ├── activity_planner_agent.py
│   ├── itinerary_planner_agent.py
│   └── travel_advisor_agent.py
├── tasks/
│   └── travel_tasks.py            # task definitions + context dependencies
├── crews/
│   ├── manager_agent.py           # delegating manager (hierarchical process)
│   └── travel_crew.py             # crew assembly + kickoff
├── tools/                         # one file per tool
│   ├── weather_tool.py            # OpenWeatherMap
│   ├── search_tool.py             # Serper web search
│   └── maps_tool.py               # Google Maps distance (optional)
├── memory/                        # read/write API used by main.py
│   ├── preferences.py
│   ├── trip_history.py
│   └── conversation.py
├── database/                      # storage layer (schemas + connection)
│   ├── models.py                  # Pydantic schemas
│   └── mongodb.py                 # single Mongo client/collections
├── utils/
│   └── formatter.py                # rich-based CLI helpers
├── .env.example
├── .gitignore
├── requirements.txt
└── LICENSE
```

---



## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# fill in your API keys and MongoDB URI in .env
```



### Required keys


| Key                                  | Used for                              | Get it from                                      |
| ------------------------------------ | ------------------------------------- | ------------------------------------------------ |
| `GEMINI_API_KEY` or `OPENAI_API_KEY` | Agent reasoning                       | Google AI Studio / OpenAI dashboard              |
| `SERPER_API_KEY`                     | Destination & hotel/restaurant search | [serper.dev](https://serper.dev)                 |
| `WEATHER_API_KEY`                    | Weather lookups                       | [openweathermap.org](https://openweathermap.org) |
| `MONGODB_URI`                        | Persistence                           | MongoDB Atlas connection string                  |
| `GOOGLE_MAPS_API_KEY`                | Distance estimates *(optional)*       | Google Cloud Console                             |


Every tool degrades gracefully if its key is missing — it returns a
placeholder string instead of crashing, so you can run the CLI before every
key is configured.

---



## Run

```bash
python main.py
```

```
1. Plan New Trip
2. View Previous Trips
3. Update Preferences
4. Exit
```

Planning a trip walks you through source, destination, budget, days,
travellers, transport, hotel tier, food preference, and interests, then hands
everything to the crew:

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

If you confirm, the trip, updated preferences, and a couple of memory notes
are saved — so the next run remembers you (*"Welcome back — I remember: ✓
Budget Hotels ✓ Vegetarian"*).

---



## How the crew fits together

```
                    Travel Planning Manager
                    (delegates + reviews)
                            │
      ┌───────────┬─────────┼─────────┬───────────┐
      ▼           ▼         ▼         ▼           ▼
   Profile    Research   Weather   Transport    Budget
      │           │         │         │           │
      └─────┬─────┴─────┬───┴───┬─────┴─────┬─────┘
            ▼            ▼      ▼           ▼
          Hotel      Restaurant       Activities
            │            │                │
            └────────────┼────────────────┘
                          ▼
                 Itinerary Planner
                          │
                          ▼
                  Travel Advisor (final output)
```

The manager assigns each task to the right specialist and can send work back
for revision; `context=[...]` on each `Task` still carries data dependencies
between steps (e.g. Budget needs Transport's estimate first).

---



## Future Improvements

- **Web frontend** — add a FastAPI + React layer on top of `run_travel_crew()` without touching the agent logic
- **Multi-city itineraries** — plan a trip across multiple destinations instead of just one
- **Structured JSON output** — have the Advisor return structured data instead of free text, for easier rendering

---
