# Imports
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import pandas
import threading
from selenium import webdriver
import string
import time
import os

# I wanted to script this in a way that would automatically update the csv's and database but I remembered that there' some issues with Player Names and repeat names for different players.
# So I just let the script export the CSV's and I'll put together an excel spreadsheet.

def player_scrape():
    full_list = pandas.DataFrame()
    # The player index uses the players last initial as the index
    player_starting_letters = list(string.ascii_lowercase)
    # Go through each letters index and get the player information
    print('[NBA Players]{} - Starting the players scrape'.format(time.strftime("%H:%M:%S",time.localtime())))
    for letter in player_starting_letters:
        # Create the link and start scraping
        print('[NBA Players]{} - Starting with players that have a last name starting with {}'.format(time.strftime("%H:%M:%S",time.localtime()),letter))
        link = 'https://www.basketball-reference.com/players/{}/'.format(letter)
        html = urlopen(link)
        soup = bs(html, 'html.parser')
        col_row = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
        # Skip the first row
        rows = soup.findAll('tr')[1:]
        info = pandas.DataFrame([[td.getText() for td in rows[i].findAll(['td','th'])]for i in range(len(rows))],columns=col_row)
        full_list = full_list.append(info,sort=False)
        print('[NBA Players]{} - Finished with players that have a last name starting with {}'.format(time.strftime("%H:%M:%S",time.localtime()),letter))
    # full_list = full_list.dropna()
    full_list.insert(0,'Player ID',range(100,100+len(full_list)))
    full_list.to_csv('NBA Players.csv',index=False)
    print('[NBA Players]{} - Finished scraping and exporting the player information'.format(time.strftime("%H:%M:%S",time.localtime())))


# Stats Scrape
def stats_scrape(year_list,links,output_tag):
    regular_season_frame = pandas.DataFrame()
    playoffs_frame = pandas.DataFrame()
    for link in links:
        for year in year_list:
            html = urlopen(link.format(year))
            soup = bs(html,'html.parser')
            # If the url is for the total stats
            if ('totals' in link): table = soup.find('table',{'id':'totals_stats'})
            # Otherwise the link poins to the per 100 possessions
            else: table = soup.find('table',{'id':'per_poss_stats'})
            rows = table.findAll('tr')
            header = [th.getText() for th in rows[0].findAll('th')][1:]
            rows = rows[1:]
            # stats = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]
            stats = []
            for i in range(len(rows)):
                data = []
                for td in rows[i].findAll('td'):
                    data.append(td.getText())
                stats.append(data)
            stats = pandas.DataFrame(stats,columns=header)
            stats = stats.dropna()
            stats.insert(0,'Season',year)
            if 'playoffs' in link:
                playoffs_frame = playoffs_frame.append(stats,sort=False)
            else:
                regular_season_frame = regular_season_frame.append(stats,sort=False)
            print('{} Finished scraping stats for the {} season'.format(output_tag,year))
    if 'Per 100' in output_tag:
        regular_season_frame.to_csv('NBA Per 100 Stats Regular Season.csv',index=False)
        playoffs_frame.to_csv('NBA Per 100 Stats Playoffs.csv',index=False)
    else:
        regular_season_frame.to_csv('NBA Total Stats Regular Season.csv',index=False)
        playoffs_frame.to_csv('NBA Total Stats Playoffs.csv',index=False)
        


# Standings Scrape
def standings_scrape(year_list):
    neutral_season = pandas.DataFrame()
    standings_frame_1 = pandas.DataFrame()
    season_change_1 = pandas.DataFrame()
    standings_frame_2 = pandas.DataFrame()
    lockout_season_1 = pandas.DataFrame()
    division_change = pandas.DataFrame()
    season_change_2 = pandas.DataFrame()
    lockout_season_2 = pandas.DataFrame()
    bubble_season = pandas.DataFrame()

    for year in year_list:
        # URL Format
        print ('[Standing Scrape]{} - Starting to scrape the standings for the {} season'.format(time.strftime("%H:%M:%S",time.localtime()),year))
        url = 'https://www.basketball-reference.com/leagues/NBA_{}_standings.html'.format(year)
        driver = webdriver.Firefox()
        driver.get(url)
        driver.minimize_window()
        # Sleep long enough to load the tables since they're populated on the backend (I think)
        time.sleep(5)
        html = driver.page_source.encode('utf-8').strip()
        soup = bs(html,'html.parser')
        # Get the expanded standings and their data
        table = soup.find('table',{'id':'expanded_standings'}) 
        # print(table)
        header = table.find('thead')
        header = header.text.replace('\n',',').replace(',,,',',')
        # Remove the empty space columns
        if (year == 1999):
            headers = header.split(',')[7:]       
        else:
            headers = header.split(',')[8:]
        while '' in headers:
            headers.remove('')
        rows = table.findAll('tr')
        # print(rows)
        standings = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]
        standings = pandas.DataFrame(standings,columns=headers)
        standings = standings.dropna(axis=0,how='all')
        standings.insert(0,'Season',year)
        # Neutral record in this season
        if (year == 1974):
            neutral_season = neutral_season.append(standings,sort=False)
        # Standard season
        elif (year in range(1975,1980) or year in range(1982,1988) or year == 1998 or year in range(2001,2005)):
            standings_frame_1 = standings_frame_1.append(standings,sort=False)
        elif (year in range(1980,1982)):
            season_change_1 = season_change_1.append(standings,sort=False)
        elif (year in range(1988,1998) or year == 2000):
            standings_frame_2 = standings_frame_2.append(standings,sort=False)
        # Lockout season for 1999
        elif (year == 1999):
            lockout_season_1 = lockout_season_1.append(standings,sort=False)
        # Season scheuled changed
        elif (year in range(2005,2007)):
            division_change = division_change.append(standings,sort=False)
        # Season schedule changed again
        elif (year in range(2007,2012) or year in range (2013,2020)):
            season_change_2 = season_change_2.append(standings,sort=False)
        # Lockout season for 2012
        elif (year == 2012):
            lockout_season_2 = lockout_season_2.append(standings,sort=False)
        # 2020 "bubble" season
        else:
            bubble_season = bubble_season.append(standings,sort=False)
        driver.quit()
        print('[Standings Scrape]{} - Finished scraping the standings for the {}'.format(time.strftime("%H:%M:%S",time.localtime()), year))
    # full_list = full_list.dropna()
    # full_list.to_csv('NBA Standings.csv',index=False)
    neutral_season.to_csv('NBA Netural Season Standings.csv',index=False)
    standings_frame_1.to_csv('NBA Standings 1.csv',index=False)
    season_change_1.to_csv('NBA Season Change 1.csv',index=False)
    standings_frame_2.to_csv('NBA Standings 2.csv',index=False)
    lockout_season_1.to_csv('NBA Lockout Season 1.csv',index=False)
    division_change.to_csv('NBA Division Change.csv',index=False)
    season_change_2.to_csv('NBA Season Change 2.csv',index=False)
    lockout_season_2.to_csv('NBA Lockout Season 2.csv',index=False)
    bubble_season.to_csv('NBA Bubble Standings.csv',index=False)
    print('[Standings Scrape]{} - Finished scraping and exporting all of the standings'.format(time.strftime("%H:%M:%S",time.localtime())))


def main():
    year_list = []
    year_list.extend(range(1974,2021))
    # Multi-threaded to kill the level of total runtime outside of the standings taking so long
    total_stats_thread = threading.Thread(target=stats_scrape,args=(year_list,['https://www.basketball-reference.com/leagues/NBA_{}_totals.html','https://www.basketball-reference.com/playoffs/NBA_{}_totals.html'],'[Totals]'))
    per_100_stats_thread = threading.Thread(target=stats_scrape,args=(year_list,['https://www.basketball-reference.com/leagues/NBA_{}_per_poss.html','https://www.basketball-reference.com/playoffs/NBA_{}_per_poss.html'],'[Per 100]'))
    player_thread = threading.Thread(target=player_scrape)
    standings_thread = threading.Thread(target=standings_scrape,args=(year_list,))
    total_stats_thread.start()
    per_100_stats_thread.start()
    player_thread.start()
    standings_thread.start()

if __name__ == "__main__":
    main()
