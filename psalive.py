import requests
from bs4 import BeautifulSoup
from tinydb import TinyDB, Query
import re

def getPlayerName(player):
    name = re.sub(r"\(.*?\)", r"", player.select('.name')[0].get_text())
    return re.sub(r"\[.*?\]", r"", name).lstrip().rstrip()

def getPlayerCountry(player):
    return re.findall(r'\((.*?)\)',player.select('.name')[0].get_text())[0]

def getPlayerSeed(player):
    seed = re.findall(r'\[(.*?)\]',player.select('.name')[0].get_text())
    if not seed:
        return ""
    else:
        return seed[0]
    
db = TinyDB("psalive.json")
all_tweets = []
url = 'https://secure.psaworldtour.com/public/live'
data = requests.get(url)
html = BeautifulSoup(data.text, 'html.parser')
tournaments = html.select('.tournament')
for tournament in tournaments:
    tournament_name = tournament.select('td.name')[0].get_text()
    tournament_round =tournament.select('td.name')[1].get_text()
    print(tournament_name + ' ' + tournament_round)
    matches = tournament.select('div.matches')
    current_round = ''
    for match in matches[0]:
        if('round' in match.attrs['class']):
            round = match.select('td.name')[0].get_text()
            round_date = match.select('td.dates')[0].get_text()
            print('*****************')
            print(round)
            current_round = round
            print(round_date)
            print('*****************')
        if('match' in match.attrs['class']):
            match_status = match.select('td.status')[0].get_text()
            match_court = match.select('.match_court')[0].get_text()
            match_time = match.select('.info span')[1].get_text()
            match_id = match.attrs['data-id']

            player = match.select('.player')[0]
            player_name = getPlayerName(player)
            player_seed = getPlayerSeed(player)
            player_country = getPlayerCountry(player)
            games_won = player.select('.games')[0].get_text()
            player1_scores = [0] * 5

            for i in range(len(player.select('.score'))):
                player1_scores[i] = player.select('.score')[i].get_text()
                print(player.select('.score')[i].get_text())
        
            player2 = match.select('.player_2')[0]
            player2_name = getPlayerName(player2)
            player2_seed = getPlayerSeed(player2)
            player2_country = getPlayerCountry(player2)
            games_won2 = player2.select('.games')[0].get_text()
            player2_scores = [0] * 5

            for i in range(len(player2.select('.score'))):
                player2_scores[i] = player2.select('.score')[i].get_text()
                print(player2.select('.score')[i].get_text())
                
            print('===================')
            print(match_status)
            print(match_court)
            print(match_time)
            print(player_name)
            print(games_won)
            print(player2_name)
            print(games_won2)
            try:
                rec = {
                    'id': match_id,
                    'tournament': tournament_name,
                    'round': current_round,
                    'match_status': match_status,
                    'match_court': match_court,
                    'match_time': match_time,
                    'player': {
                        'name': player_name,
                        'seed': player_seed,
                        'country': player_country,
                        'games_won': games_won,
                        'game1': player1_scores[0],
                        'game2': player1_scores[1],
                        'game3': player1_scores[2],
                        'game4': player1_scores[3],
                        'game5': player1_scores[4],
                    },
                    'player2': {
                        'name': player2_name,
                        'seed': player2_seed,
                        'country': player2_country,
                        'games_won': games_won2,
                        'game1': player2_scores[0],
                        'game2': player2_scores[1],
                        'game3': player2_scores[2],
                        'game4': player2_scores[3],
                        'game5': player2_scores[4],
                    },
                    # 'createdt': datetime.datetime.now().isoformat()
                }

                Result = Query()
                s1 = db.search(Result.id == rec["id"])

                if not s1:
                    # total_added += 1
                    # print ("Adding ... ", total_added)
                    db.insert(rec)

            except (AttributeError, KeyError) as ex:
                pass