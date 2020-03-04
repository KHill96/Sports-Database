# Imports
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import pandas
import threading
from selenium import webdriver
import string

def playerScrape():
    # Create a list for the data frames
    frames =[]

    # The player index uses the players last initial as the index
    # There's never been a player with a last name starting with x so I just got rid of it to avoid any errors
    playerStartingLetters = list(string.ascii_lowercase)
    playerStartingLetters.pop(23)

    # Go through each letters index and get the player information
    for letter in playerStartingLetters:

        # Create the link and start scraping
        link = 'https://www.basketball-reference.com/players/{}/'.format(letter)
        html = urlopen(link)
        soup = bs(html, 'html.parser')

        # Get the column names
        colRow = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
        # Skip the first row
        rows = soup.findAll('tr')[1:]
        # Get their info and put it into the frame
        info = pandas.DataFrame([[td.getText() for td in rows[i].findAll(['td','th'])]for i in range(len(rows))],columns=colRow)
        # add the frame to the list
        frames.append(info)

    # Put the frames together
    pandas.concat(frames).to_csv('Players.csv',index=False)
    print("Players Scrape Done")

def totalStats_Scrape(yearList = [], *args):
    fullList = pandas.DataFrame()
    for year in yearList:
        url = 'https://www.basketball-reference.com/leagues/NBA_{}_totals.html'.format(year)
        html = urlopen(url)
        soup = bs(html,'html.parser')
        table = soup.find('table',{'id':'totals_stats'})
        # header = [table.find('tr').findAll('th')]
        rows = table.findAll('tr')
        header = [th.getText() for th in rows[0].findAll('th')]
        header = header[1:]
        rows = rows[1:]
        totalStats = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]
        totalStats = pandas.DataFrame(totalStats, columns=header)
        totalStats.insert(0,'Season',year)
        fullList = fullList.append(totalStats,sort=False)
        # print('{} total stats done'.format(year))
    print('Total Stats done')
    fullList.to_csv('Total Stats.csv',index=False)

def standingsScrape(yearList = [], *args):
    fullList = pandas.DataFrame()
    for year in yearList:
        # URL Format
        url = 'https://www.basketball-reference.com/leagues/NBA_{}_standings.html'.format(year)
        # Change path to geckodriver.exe       
        driver = webdriver.Firefox(executable_path='C:\\Users\\could\\Documents\\geckodriver.exe')
        driver.get(url)
        driver.minimize_window()
        # Sleep long enough to load the tables since they're populated on the backend (I think)
        time.sleep(5)
        html = driver.page_source.encode('utf-8').strip()
        soup = bs(html,'html.parser')
        # Get the expanded standings and their data
        table = soup.find('table',{'id':'expanded_standings'})
        header = table.find('thead')
        header = header.text.replace('\n','')
        headers = header.split(',,,')
        headerRow = headers[2]
        headerRow = headerRow.split(',')
        # Remove the empty space columns and Rk column
        while '' in headerRow:
            headerRow.remove('')
        headerRow.remove('Rk')
        # Build the data frame
        rows = table.findAll('tr')
        standings = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]
        standings = pandas.DataFrame(standings,columns=headerRow)
        # Add the season to the frame
        standings.insert(0,'Season',year,False)
        driver.quit()
        fullList = fullList.append(standings,sort=False)
    fullList.to_csv('Standings.csv',index=False)
    print('Standings Scrape Done')

def per100Stats_Scrape(yearList = [], *args):
    fullList = pandas.DataFrame()
    for year in yearList:
        url ='https://www.basketball-reference.com/leagues/NBA_{}_per_poss.html'.format(year)        
        html = urlopen(url)
        soup = bs(html,'html.parser')
        table = soup.find('table',{'id':'per_poss_stats'})
        # header = [table.find('tr').findAll('th')]
        rows = table.findAll('tr')
        header = [th.getText() for th in rows[0].findAll('th')]
        header = header[1:]
        rows = rows[1:]
        totalStats = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]
        totalStats = pandas.DataFrame(totalStats, columns=header)
        totalStats.insert(0,'Season',year)
        fullList = fullList.append(totalStats,sort=False)
        # print('{} per 100 done'.format(year))
    print('Per 100 Stats done')
    fullList.to_csv('Per 100 Stats.csv',index=False)

def main():
    # Create a list of years from 1974 to 2019 since the 2019-2020 only just got started a few weeks ago
    yearList = []
    yearList.extend(range(1974,2021))

    # I'm using threads so it wont take so much time. They can scrape concurrently
    totalStatsThread = threading.Thread(target=totalStats_Scrape,args=(yearList,))
    per100StatsThread = threading.Thread(target=per100Stats_Scrape,args=(yearList,))
    playerThread = threading.Thread(target=playerScrape)
    standingsThread = threading.Thread(target=standingsScrape,args=(yearList,))
    totalStatsThread.start()
    per100StatsThread.start()
    playerThread.start()
    standingsThread.start()

if __name__ == "__main__":
    main()
