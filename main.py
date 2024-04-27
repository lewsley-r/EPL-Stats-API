from fastapi import FastAPI
from selectolax.parser import HTMLParser
import httpx

app = FastAPI()


def get_stat(endpoint_postfix, stat_name, club_or_player):
    url = f"https://www.premierleague.com/stats/top/{endpoint_postfix}"
    headers = {
        "user-agent": "mozilla/5.0 (x11; linux x86_64) applewebkit/537.36 (khtml, like gecko) chrome/123.0.0.0 safari/537.36"}
    resp = httpx.get(url, headers=headers)
    html = HTMLParser(resp.text)
    stats = html.css("tr.table__row")
    if club_or_player == 'club':
        clubs = []
        for club in stats:
            item = club.text().replace('\n', '')
            items = list(filter(None, item.split('  ')))
            club_profile = {'Rank': items[0],
                            'Name': items[1], stat_name: items[2]}
            clubs.append(club_profile)
        return clubs
    elif club_or_player == 'player':
        players = []
        for player in stats:
            item = player.text().replace('\n', '')
            items = list(filter(None, item.split('  ')))
            player_profile = {'Rank': items[0], 'Player Name': items[1], 'Club': items[2],
                              'Nationality': items[3], stat_name: items[4]}
            players.append(player_profile)
        return players


@app.get("/player/goals")
def get_top_10_players_by_goals():
    return get_stat('players/goals', 'Goals', 'player')


@app.get("/player/assists")
def get_top_10_players_by_assists():
    return get_stat('players/goal_assist', 'Assists', 'player')


@app.get("/player/shots")
def get_top_10_players_by_shots():
    return get_stat('players/total_scoring_att', 'Shots', 'player')


@app.get("/player/clean_sheets")
def get_top_10_players_by_clean_sheets():
    return get_stat('players/clean_sheet', ' Clean Sheets', 'player')


@app.get("/player/saves")
def get_top_10_players_by_saves():
    return get_stat('players/saves?po=GOALKEEPER', 'Saves', 'player')
