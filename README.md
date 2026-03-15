# College Football Data MCP Server

An MCP (Model Context Protocol) server that exposes all [College Football Data API](https://api.collegefootballdata.com) endpoints as tools, enabling AI agents to query college football stats, ratings, recruiting data, game results, and more.

---

## Requirements

- Python 3.10+
- `httpx`
- `mcp[cli]` (FastMCP)

Install dependencies:
```bash
pip install httpx "mcp[cli]"
```

---

## Running the Server

```bash
python API.py
```

The server starts on `http://0.0.0.0:8500` using the **Streamable HTTP** transport.

MCP endpoint: `http://localhost:8500/mcp`

---

## Authentication

All tools accept an optional `api_key` parameter. A default key is pre-configured, but you can override it per call:

```python
get_games(year=2023, team="Alabama", api_key="YOUR_API_KEY")
```

Get your free API key at [collegefootballdata.com](https://collegefootballdata.com).

---

## Available Tools

### Adjusted Metrics

| Tool | Description |
|------|-------------|
| `get_adjusted_team_season_metrics` | Opponent-adjusted team season statistics (WEPA) |
| `get_adjusted_player_passing` | Opponent-adjusted player passing statistics |
| `get_adjusted_player_rushing` | Opponent-adjusted player rushing statistics |
| `get_adjusted_player_kicking` | Points Added Above Replacement (PAAR) for kickers |

---

### Teams

| Tool | Description |
|------|-------------|
| `get_teams` | General team information |
| `get_fbs_teams` | FBS teams (highest division) |
| `get_team_matchup` | Historical head-to-head matchup details |
| `get_teams_ats` | Against-the-spread (ATS) summary by team |
| `get_roster` | Historical roster data |

---

### Conferences & Venues

| Tool | Description |
|------|-------------|
| `get_conferences` | List of all conferences |
| `get_venues` | List of venues with capacity and location |

---

### Talent & Team Stats

| Tool | Description |
|------|-------------|
| `get_talent` | 247 Team Talent Composite for a given year |
| `get_season_stats` | Aggregated team season statistics |
| `get_advanced_season_stats` | Advanced team season stats with offense/defense breakdown |
| `get_advanced_game_stats` | Advanced statistics aggregated by game |
| `get_game_havoc_stats` | Havoc statistics aggregated by game |
| `get_stat_categories` | Available team statistical categories |

---

### Player Statistics

| Tool | Description |
|------|-------------|
| `get_player_season_stats` | Aggregated player statistics for a season |
| `search_players` | Search for players by name |
| `get_player_usage` | Player snap usage breakdowns |

---

### Recruiting

| Tool | Description |
|------|-------------|
| `get_recruiting_players` | Player recruiting rankings |
| `get_recruiting_teams` | Team recruiting rankings |
| `get_recruiting_groups` | Aggregated recruiting by team and position group |

---

### Ratings

| Tool | Description |
|------|-------------|
| `get_sp_ratings` | SP+ ratings for a year or school |
| `get_sp_conference_ratings` | Historical conference SP+ data |
| `get_srs_ratings` | Historical SRS ratings |
| `get_elo_ratings` | Historical Elo ratings |
| `get_fpi_ratings` | Football Power Index (FPI) ratings |

---

### Rankings & Polls

| Tool | Description |
|------|-------------|
| `get_rankings` | Historical poll data (AP, Coaches, CFP, etc.) |

---

### Plays & Game Data

| Tool | Description |
|------|-------------|
| `get_plays` | Historical play-by-play data |
| `get_play_types` | Available play types |
| `get_play_stats` | Player-play associations (limit 2000) |

---

### Predicted Points (PPA)

| Tool | Description |
|------|-------------|
| `get_predicted_points` | Expected points by field position |
| `get_team_ppa_season` | Team season predicted points added |
| `get_team_ppa_game` | Game-level team predicted points added |
| `get_player_ppa_season` | Player season predicted points added |
| `get_player_ppa_game` | Player game-level predicted points added |

---

### Win Probability

| Tool | Description |
|------|-------------|
| `get_pregame_win_probability` | Pregame win probability |
| `get_play_win_probability` | Play-by-play win probability |

---

### Game Information

| Tool | Description |
|------|-------------|
| `get_games` | Game schedules and results |
| `get_game_media` | Broadcast information (TV, radio) |
| `get_game_weather` | Historical weather conditions per game |
| `get_game_team_stats` | Team-level statistics for a specific game |
| `get_game_player_stats` | Player-level statistics for a specific game |
| `get_advanced_box_score` | Advanced box score with team/player analytics |

---

### Live Games

| Tool | Description |
|------|-------------|
| `get_live_games` | Live scoreboard with real-time plays and drives |

---

### Betting

| Tool | Description |
|------|-------------|
| `get_betting_lines` | Betting lines (spread, moneyline, over/under) |

---

### Records, Calendar & Coaches

| Tool | Description |
|------|-------------|
| `get_records` | Team season records and standings |
| `get_calendar` | Season calendar weeks |
| `get_coaches` | Coaching history and season records |

---

### Draft, Transfers & Returning Production

| Tool | Description |
|------|-------------|
| `get_draft_picks` | NFL draft picks from college players |
| `get_returning_production` | Team returning production analysis |
| `get_transfers` | Transfer portal player movements |

---

### User

| Tool | Description |
|------|-------------|
| `get_user_info` | API account info (patron level, remaining calls) |

---

## Connecting an AI Agent

To connect an ADK-based agent to this MCP server, use `StreamableHTTPConnectionParams`:

```python
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

tools = [
    McpToolset(
        connection_params=StreamableHTTPConnectionParams(
            url="http://localhost:8500/mcp"
        )
    )
]
```

---

## Example Tool Calls

```python
# Get Alabama's 2023 schedule
get_games(year=2023, team="Alabama")

# Search for a player
search_players(search_term="Bryce Young")

# Get AP Top 25 for week 10, 2022
get_rankings(year=2022, week=10)

# Get betting lines for a specific week
get_betting_lines(year=2023, week=5, season_type="regular")

# Get head-to-head history: Alabama vs Auburn
get_team_matchup(team1="Alabama", team2="Auburn")

# Get live scoreboard
get_live_games()
```

---

## Project Structure

```
CollegeFootballMCPServer/
├── API.py                     # MCP server with all 52 tools
├── main.py                    # FastAPI WebSocket + ADK agent server
├── mcp_server/
│   └── collegefootball.py     # Standalone MCP server (alternate entry)
└── README.md                  # This file
```

---

## Environment Setup

Create a `.env` file with your Google Cloud credentials for the ADK agent:

```bash
# Choose Model Backend: 0 -> Gemini Developer API, 1 -> Vertex AI
GOOGLE_GENAI_USE_VERTEXAI=1

# Vertex AI backend config
GOOGLE_CLOUD_PROJECT="your-project-id"
GOOGLE_CLOUD_LOCATION="us-central1"
```

Then start the agent server:

```bash
uvicorn main:app --reload --port 8080
```
