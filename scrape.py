import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
import time



# league_codes = {'Premier League': 9,
#                 'Liga': 12,
#                 'Bundesliga': 20,
#                 'Serie A': 11}

# league_codes = {'Eredivise': 23,
#                 'Primeira Liga': 32}

league_codes = {'Premier League': 9}
            

def scrape_league_games(league) :

    years = np.arange(1996, 2024 + 1)
    dfs = []
    for year in years :
  
        print(f'Scraping {league} games... {year-1}-{year}...          ', end = '\r')
        time.sleep(5)
        url = f'https://fbref.com/en/comps/{league_codes.get(league)}/{year-1}-{year}/schedule/'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'lxml')
        table = soup.find('table')

        games = pd.read_html(str(table))[0]
        games = games[games['Score'].notna()].reset_index(drop = True)
        games['G_home'] = games['Score'].apply(lambda x: x.split('–')[0])
        games['G_away'] = games['Score'].apply(lambda x: x.split('–')[-1])
        games['Home_W'] = (games['G_home'] > games['G_away']).astype(int)
        games['Draw'] = (games['G_home'] == games['G_away']).astype(int)
        games['Away_W'] = (games['G_home'] < games['G_away']).astype(int)
        games['League'] = league
        games['Year'] = year
        games = games[['Year', 'League', 'Date', 'Time', 'Home', 'Away', 'G_home', 'G_away', 'Home_W', 'Draw', 'Away_W', 'Venue', 'Attendance']]
        dfs.append(games)
    
    output = pd.concat(dfs)
    output.to_csv('data/' + league.replace(' ', '-') + '_' + str(min(years)-1) + '-' + str(year) + '.csv', index = None)


for league in league_codes.keys() :
    scrape_league_games(league)