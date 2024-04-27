from fastapi import FastAPI
from selectolax.parser import HTMLParser
import httpx

app = FastAPI()


def get_stat(endpoint_postfix):
    url = f"https://www.premierleague.com/stats/top/{endpoint_postfix}"
    headers = {
        "user-agent": "mozilla/5.0 (x11; linux x86_64) applewebkit/537.36 (khtml, like gecko) chrome/123.0.0.0 safari/537.36"}
    resp = httpx.get(url, headers=headers)
    html = HTMLParser(resp.text)
    stat = html.css("tr.table__row")
    return stat


@app.get("/player/goals")
def get_top_10_players_by_goals():
    player_goals = get_stat('players/goals')
    players = []
    for player in player_goals:
        item = player.text().replace('\n', '')
        items = list(filter(None, item.split('  ')))
        player_profile = {'Rank': items[0], 'Player Name': items[1], 'Club': items[2],
                          'Nationality': items[3], 'Goals': items[4]}
        players.append(player_profile)
    return players


@app.get("/player/assists")
def get_top_10_players_by_assists():
    player_assists = get_stat('players/goal_assist')
    players = []
    for player in player_assists:
        item = player.text().replace('\n', '')
        items = list(filter(None, item.split('  ')))
        player_profile = {'Rank': items[0], 'Player Name': items[1], 'Club': items[2],
                          'Nationality': items[3], 'Assists': items[4]}
        players.append(player_profile)
    return players
