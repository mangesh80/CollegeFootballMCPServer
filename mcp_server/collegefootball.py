"""
College Football Data API - Python Client
All endpoints from https://api.collegefootballdata.com
Requires a Bearer token from https://collegefootballdata.com
"""

import httpx
from typing import Optional
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("collegefbMCPServer", host="0.0.0.0", port=8500)

API_BASE_URL = "https://api.collegefootballdata.com"
DEFAULT_API_KEY = "g3XHK8w/mh2g7YYk/d/yWSuCJRKnM52/IG7J/lN9Q+h3xz3k/Dg1sQpPwNOSNs0W"


def _get_headers(api_key: str) -> dict:
    return {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}


def _get(endpoint: str, params: dict, api_key: str) -> list | dict:
    """Internal helper to make GET requests."""
    # Remove None values from params
    params = {k: v for k, v in params.items() if v is not None}
    response = httpx.get(
        f"{API_BASE_URL}{endpoint}",
        headers=_get_headers(api_key),
        params=params
    )
    response.raise_for_status()
    return response.json()


# ---------------------------------------------------------------------------
# ADJUSTED METRICS
# ---------------------------------------------------------------------------

@mcp.tool()
def get_adjusted_team_season_metrics(
    year: Optional[int] = None,
    team: Optional[str] = None,
    conference: Optional[str] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Opponent-adjusted team season statistics (WEPA)."""
    return _get("/wepa/team/season", {"year": year, "team": team, "conference": conference}, api_key)


@mcp.tool()
def get_adjusted_player_passing(
    year: Optional[int] = None,
    team: Optional[str] = None,
    conference: Optional[str] = None,
    position: Optional[str] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Opponent-adjusted player passing statistics."""
    return _get("/wepa/players/passing", {"year": year, "team": team, "conference": conference, "position": position}, api_key)


@mcp.tool()
def get_adjusted_player_rushing(
    year: Optional[int] = None,
    team: Optional[str] = None,
    conference: Optional[str] = None,
    position: Optional[str] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Opponent-adjusted player rushing statistics."""
    return _get("/wepa/players/rushing", {"year": year, "team": team, "conference": conference, "position": position}, api_key)


@mcp.tool()
def get_adjusted_player_kicking(
    year: Optional[int] = None,
    team: Optional[str] = None,
    conference: Optional[str] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Points Added Above Replacement (PAAR) ratings for kickers."""
    return _get("/wepa/players/kicking", {"year": year, "team": team, "conference": conference}, api_key)


# ---------------------------------------------------------------------------
# TEAMS
# ---------------------------------------------------------------------------

@mcp.tool()
def get_teams(
    conference: Optional[str] = None,
    year: Optional[int] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """General team information."""
    return _get("/teams", {"conference": conference, "year": year}, api_key)


@mcp.tool()
def get_fbs_teams(
    year: Optional[int] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Information on FBS teams (highest division)."""
    return _get("/teams/fbs", {"year": year}, api_key)


@mcp.tool()
def get_team_matchup(
    team1: str,
    team2: str,
    min_year: Optional[int] = None,
    max_year: Optional[int] = None,
    api_key: str = DEFAULT_API_KEY
) -> dict:
    """Historical matchup details for two given teams."""
    return _get("/teams/matchup", {"team1": team1, "team2": team2, "minYear": min_year, "maxYear": max_year}, api_key)


@mcp.tool()
def get_teams_ats(
    year: int,
    conference: Optional[str] = None,
    team: Optional[str] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Against-the-spread (ATS) summary by team."""
    return _get("/teams/ats", {"year": year, "conference": conference, "team": team}, api_key)


@mcp.tool()
def get_roster(
    team: Optional[str] = None,
    year: Optional[int] = None,
    classification: Optional[str] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Historical roster data."""
    return _get("/roster", {"team": team, "year": year, "classification": classification}, api_key)


# ---------------------------------------------------------------------------
# CONFERENCES & VENUES
# ---------------------------------------------------------------------------

@mcp.tool()
def get_conferences(api_key: str = DEFAULT_API_KEY) -> list:
    """List of conferences."""
    return _get("/conferences", {}, api_key)


@mcp.tool()
def get_venues(api_key: str = DEFAULT_API_KEY) -> list:
    """List of venues with capacity and location details."""
    return _get("/venues", {}, api_key)


# ---------------------------------------------------------------------------
# TALENT & TEAM STATS
# ---------------------------------------------------------------------------

@mcp.tool()
def get_talent(
    year: int,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """247 Team Talent Composite for a given year."""
    return _get("/talent", {"year": year}, api_key)


@mcp.tool()
def get_season_stats(
    year: Optional[int] = None,
    team: Optional[str] = None,
    conference: Optional[str] = None,
    start_week: Optional[int] = None,
    end_week: Optional[int] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Aggregated team season statistics. Requires year or team."""
    return _get("/stats/season", {
        "year": year, "team": team, "conference": conference,
        "startWeek": start_week, "endWeek": end_week
    }, api_key)


@mcp.tool()
def get_advanced_season_stats(
    year: Optional[int] = None,
    team: Optional[str] = None,
    exclude_garbage_time: Optional[bool] = None,
    start_week: Optional[int] = None,
    end_week: Optional[int] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Advanced season statistics for teams. Requires year or team."""
    return _get("/stats/season/advanced", {
        "year": year, "team": team, "excludeGarbageTime": exclude_garbage_time,
        "startWeek": start_week, "endWeek": end_week
    }, api_key)


@mcp.tool()
def get_advanced_game_stats(
    year: Optional[int] = None,
    team: Optional[str] = None,
    week: Optional[int] = None,
    opponent: Optional[str] = None,
    exclude_garbage_time: Optional[bool] = None,
    season_type: Optional[str] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Advanced statistics aggregated by game. Requires year or team."""
    return _get("/stats/game/advanced", {
        "year": year, "team": team, "week": week, "opponent": opponent,
        "excludeGarbageTime": exclude_garbage_time, "seasonType": season_type
    }, api_key)


@mcp.tool()
def get_game_havoc_stats(
    year: Optional[int] = None,
    team: Optional[str] = None,
    week: Optional[int] = None,
    opponent: Optional[str] = None,
    season_type: Optional[str] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Havoc statistics aggregated by game. Requires year or team."""
    return _get("/stats/game/havoc", {
        "year": year, "team": team, "week": week,
        "opponent": opponent, "seasonType": season_type
    }, api_key)


@mcp.tool()
def get_stat_categories(api_key: str = DEFAULT_API_KEY) -> list:
    """List of team statistical categories."""
    return _get("/stats/categories", {}, api_key)


# ---------------------------------------------------------------------------
# PLAYER STATISTICS
# ---------------------------------------------------------------------------

@mcp.tool()
def get_player_season_stats(
    year: int,
    conference: Optional[str] = None,
    team: Optional[str] = None,
    start_week: Optional[int] = None,
    end_week: Optional[int] = None,
    season_type: Optional[str] = None,
    category: Optional[str] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Aggregated player statistics for a given season."""
    return _get("/stats/player/season", {
        "year": year, "conference": conference, "team": team,
        "startWeek": start_week, "endWeek": end_week,
        "seasonType": season_type, "category": category
    }, api_key)


@mcp.tool()
def search_players(
    search_term: str,
    position: Optional[str] = None,
    team: Optional[str] = None,
    year: Optional[int] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Search for players by name."""
    return _get("/player/search", {
        "searchTerm": search_term, "position": position,
        "team": team, "year": year
    }, api_key)


@mcp.tool()
def get_player_usage(
    year: Optional[int] = None,
    team: Optional[str] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Player snap usage breakdowns."""
    return _get("/player/usage", {"year": year, "team": team}, api_key)


# ---------------------------------------------------------------------------
# RECRUITING
# ---------------------------------------------------------------------------

@mcp.tool()
def get_recruiting_players(
    year: Optional[int] = None,
    team: Optional[str] = None,
    position: Optional[str] = None,
    state: Optional[str] = None,
    classification: Optional[str] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Player recruiting rankings. Requires year or team."""
    return _get("/recruiting/players", {
        "year": year, "team": team, "position": position,
        "state": state, "classification": classification
    }, api_key)


@mcp.tool()
def get_recruiting_teams(
    year: Optional[int] = None,
    team: Optional[str] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Team recruiting rankings."""
    return _get("/recruiting/teams", {"year": year, "team": team}, api_key)


@mcp.tool()
def get_recruiting_groups(
    team: Optional[str] = None,
    conference: Optional[str] = None,
    recruit_type: Optional[str] = None,
    start_year: Optional[int] = None,
    end_year: Optional[int] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Aggregated recruiting statistics by team and position grouping."""
    return _get("/recruiting/groups", {
        "team": team, "conference": conference, "recruitType": recruit_type,
        "startYear": start_year, "endYear": end_year
    }, api_key)


# ---------------------------------------------------------------------------
# RATINGS
# ---------------------------------------------------------------------------

@mcp.tool()
def get_sp_ratings(
    year: Optional[int] = None,
    team: Optional[str] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """SP+ ratings for a given year or school. Requires year or team."""
    return _get("/ratings/sp", {"year": year, "team": team}, api_key)


@mcp.tool()
def get_sp_conference_ratings(
    year: Optional[int] = None,
    conference: Optional[str] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Aggregated historical conference SP+ data."""
    return _get("/ratings/sp/conferences", {"year": year, "conference": conference}, api_key)


@mcp.tool()
def get_srs_ratings(
    year: Optional[int] = None,
    team: Optional[str] = None,
    conference: Optional[str] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Historical SRS ratings for a year or team. Requires year or team."""
    return _get("/ratings/srs", {"year": year, "team": team, "conference": conference}, api_key)


@mcp.tool()
def get_elo_ratings(
    year: Optional[int] = None,
    week: Optional[int] = None,
    season_type: Optional[str] = None,
    team: Optional[str] = None,
    conference: Optional[str] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Historical Elo ratings."""
    return _get("/ratings/elo", {
        "year": year, "week": week, "seasonType": season_type,
        "team": team, "conference": conference
    }, api_key)


@mcp.tool()
def get_fpi_ratings(
    year: Optional[int] = None,
    team: Optional[str] = None,
    conference: Optional[str] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Historical Football Power Index (FPI) ratings. Requires year or team."""
    return _get("/ratings/fpi", {"year": year, "team": team, "conference": conference}, api_key)


# ---------------------------------------------------------------------------
# RANKINGS & POLLS
# ---------------------------------------------------------------------------

@mcp.tool()
def get_rankings(
    year: int,
    season_type: Optional[str] = None,
    week: Optional[int] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Historical poll data (AP, Coaches, CFP, etc.)."""
    return _get("/rankings", {"year": year, "seasonType": season_type, "week": week}, api_key)


# ---------------------------------------------------------------------------
# PLAYS & GAME DATA
# ---------------------------------------------------------------------------

@mcp.tool()
def get_plays(
    year: int,
    week: int,
    team: Optional[str] = None,
    offense: Optional[str] = None,
    defense: Optional[str] = None,
    offense_conference: Optional[str] = None,
    defense_conference: Optional[str] = None,
    conference: Optional[str] = None,
    play_type: Optional[int] = None,
    season_type: Optional[str] = None,
    classification: Optional[str] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Historical play-by-play data."""
    return _get("/plays", {
        "year": year, "week": week, "team": team, "offense": offense, "defense": defense,
        "offenseConference": offense_conference, "defenseConference": defense_conference,
        "conference": conference, "playType": play_type, "seasonType": season_type,
        "classification": classification
    }, api_key)


@mcp.tool()
def get_play_types(api_key: str = DEFAULT_API_KEY) -> list:
    """Available play types."""
    return _get("/plays/types", {}, api_key)


@mcp.tool()
def get_play_stats(
    year: Optional[int] = None,
    week: Optional[int] = None,
    team: Optional[str] = None,
    game_id: Optional[int] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Player-play associations (limit 2000)."""
    return _get("/plays/stats", {"year": year, "week": week, "team": team, "gameId": game_id}, api_key)


# ---------------------------------------------------------------------------
# PREDICTED POINTS (PPA)
# ---------------------------------------------------------------------------

@mcp.tool()
def get_predicted_points(
    year: Optional[int] = None,
    team: Optional[str] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Expected points by field position."""
    return _get("/ppa/predicted-points", {"year": year, "team": team}, api_key)


@mcp.tool()
def get_team_ppa_season(
    year: Optional[int] = None,
    team: Optional[str] = None,
    start_week: Optional[int] = None,
    end_week: Optional[int] = None,
    exclude_garbage_time: Optional[bool] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Team season predicted points added. Requires year or team."""
    return _get("/ppa/team/season", {
        "year": year, "team": team, "startWeek": start_week,
        "endWeek": end_week, "excludeGarbageTime": exclude_garbage_time
    }, api_key)


@mcp.tool()
def get_team_ppa_game(
    year: Optional[int] = None,
    team: Optional[str] = None,
    week: Optional[int] = None,
    opponent: Optional[str] = None,
    season_type: Optional[str] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Game-level team predicted points added. Requires year or team."""
    return _get("/ppa/team/game", {
        "year": year, "team": team, "week": week,
        "opponent": opponent, "seasonType": season_type
    }, api_key)


@mcp.tool()
def get_player_ppa_season(
    year: Optional[int] = None,
    team: Optional[str] = None,
    conference: Optional[str] = None,
    position: Optional[str] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Player season predicted points added. Requires year or team."""
    return _get("/ppa/players/season", {
        "year": year, "team": team, "conference": conference, "position": position
    }, api_key)


@mcp.tool()
def get_player_ppa_game(
    year: Optional[int] = None,
    team: Optional[str] = None,
    week: Optional[int] = None,
    season_type: Optional[str] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Player game-level predicted points added. Requires year or team."""
    return _get("/ppa/players/games", {
        "year": year, "team": team, "week": week, "seasonType": season_type
    }, api_key)


# ---------------------------------------------------------------------------
# WIN PROBABILITY
# ---------------------------------------------------------------------------

@mcp.tool()
def get_pregame_win_probability(
    year: Optional[int] = None,
    week: Optional[int] = None,
    season_type: Optional[str] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Pregame win probability."""
    return _get("/wp/pregame", {"year": year, "week": week, "seasonType": season_type}, api_key)


@mcp.tool()
def get_play_win_probability(
    game_id: Optional[int] = None,
    year: Optional[int] = None,
    week: Optional[int] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Play-by-play win probability."""
    return _get("/wp/plays", {"gameId": game_id, "year": year, "week": week}, api_key)


# ---------------------------------------------------------------------------
# GAME INFORMATION
# ---------------------------------------------------------------------------

@mcp.tool()
def get_games(
    year: Optional[int] = None,
    week: Optional[int] = None,
    season_type: Optional[str] = None,
    team: Optional[str] = None,
    conference: Optional[str] = None,
    division: Optional[str] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Game schedules and results."""
    return _get("/games", {
        "year": year, "week": week, "seasonType": season_type,
        "team": team, "conference": conference, "division": division
    }, api_key)


@mcp.tool()
def get_game_media(
    year: Optional[int] = None,
    week: Optional[int] = None,
    season_type: Optional[str] = None,
    team: Optional[str] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Game broadcast information (TV, radio)."""
    return _get("/games/media", {
        "year": year, "week": week, "seasonType": season_type, "team": team
    }, api_key)


@mcp.tool()
def get_game_weather(
    year: Optional[int] = None,
    week: Optional[int] = None,
    season_type: Optional[str] = None,
    team: Optional[str] = None,
    conference: Optional[str] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Historical game weather conditions (temperature, wind, precipitation)."""
    return _get("/games/weather", {
        "year": year, "week": week, "seasonType": season_type,
        "team": team, "conference": conference
    }, api_key)


@mcp.tool()
def get_game_team_stats(
    game_id: int,
    api_key: str = DEFAULT_API_KEY
) -> dict:
    """Team-level statistics for a specific game."""
    return _get("/games/teams", {"gameId": game_id}, api_key)


@mcp.tool()
def get_game_player_stats(
    game_id: int,
    api_key: str = DEFAULT_API_KEY
) -> dict:
    """Player-level statistics for a specific game."""
    return _get("/games/players", {"gameId": game_id}, api_key)


@mcp.tool()
def get_advanced_box_score(
    game_id: int,
    api_key: str = DEFAULT_API_KEY
) -> dict:
    """Advanced game box score statistics with team/player analytics."""
    return _get("/box-score", {"gameId": game_id}, api_key)


# ---------------------------------------------------------------------------
# LIVE GAMES
# ---------------------------------------------------------------------------

@mcp.tool()
def get_live_games(api_key: str = DEFAULT_API_KEY) -> list:
    """Live game scoreboard data with real-time plays and drives."""
    return _get("/live/games", {}, api_key)


# ---------------------------------------------------------------------------
# BETTING
# ---------------------------------------------------------------------------

@mcp.tool()
def get_betting_lines(
    year: Optional[int] = None,
    week: Optional[int] = None,
    season_type: Optional[str] = None,
    team: Optional[str] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Betting line data (spread, moneyline, over/under)."""
    return _get("/lines", {
        "year": year, "week": week, "seasonType": season_type, "team": team
    }, api_key)


# ---------------------------------------------------------------------------
# RECORDS, CALENDAR & COACHES
# ---------------------------------------------------------------------------

@mcp.tool()
def get_records(
    year: Optional[int] = None,
    team: Optional[str] = None,
    conference: Optional[str] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Team season records and standings."""
    return _get("/records", {"year": year, "team": team, "conference": conference}, api_key)


@mcp.tool()
def get_calendar(
    year: Optional[int] = None,
    season_type: Optional[str] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Season calendar weeks."""
    return _get("/calendar", {"year": year, "seasonType": season_type}, api_key)


@mcp.tool()
def get_coaches(
    team: Optional[str] = None,
    year: Optional[int] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Coaching history and season records."""
    return _get("/coaches", {"team": team, "year": year}, api_key)


# ---------------------------------------------------------------------------
# DRAFT, TRANSFERS & RETURNING PRODUCTION
# ---------------------------------------------------------------------------

@mcp.tool()
def get_draft_picks(
    year: Optional[int] = None,
    team: Optional[str] = None,
    college: Optional[str] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """NFL draft picks from college players."""
    return _get("/draft", {"year": year, "team": team, "college": college}, api_key)


@mcp.tool()
def get_returning_production(
    year: Optional[int] = None,
    team: Optional[str] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Team returning production analysis."""
    return _get("/returning-production", {"year": year, "team": team}, api_key)


@mcp.tool()
def get_transfers(
    year: Optional[int] = None,
    team: Optional[str] = None,
    season: Optional[str] = None,
    api_key: str = DEFAULT_API_KEY
) -> list:
    """Transfer portal player movements."""
    return _get("/transfers", {"year": year, "team": team, "season": season}, api_key)


# ---------------------------------------------------------------------------
# USER
# ---------------------------------------------------------------------------

@mcp.tool()
def get_user_info(api_key: str = DEFAULT_API_KEY) -> dict:
    """API user account information (patron level, remaining calls)."""
    return _get("/user", {}, api_key)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
