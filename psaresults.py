import requests
from bs4 import BeautifulSoup
from tinydb import TinyDB, Query

db = TinyDB("psaresults.json")
all_tweets = []
url = 'https://secure.psaworldtour.com/public/results'
data = requests.get(url)
html = BeautifulSoup(data.text, 'html.parser')
tournaments = html.select('.tournament')
for tournament in tournaments:
    tournament_name = tournament.select('td.name')
    tournament_round = tournament_name[1].get_text()
    print(tournament_name[0].get_text() + ' ' + tournament_round)
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
            match_name = match.select('td.match')[0].get_text()
            match_score = match.select('.scores')[0].get_text()
            match_id = match.attrs['data-id']
            print('===================')
            print(match_name)
            print(match_score)
            print(match_id)
            try:
                rec = {
                    'id': match_id,
                    'tournament': tournament_name,
                    'match_name': match_name,
                    'match_score': match_score,
                    'current_round': current_round,
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