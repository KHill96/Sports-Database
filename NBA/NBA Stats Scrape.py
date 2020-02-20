# Imports
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import pandas
import threading

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
        print('{} total stats done'.format(year))
    print('Total Stats done')
    fileName = 'Total Stats.csv'
    fullList.to_csv(fileName,index=False)

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
        print('{} per 100 done'.format(year))
    print('Per 100 Stats done')
    fileName = 'Per 100 Stats.csv'
    fullList.to_csv(fileName,index=False)

def main():
    # Create a list of years from 1974 to 2019 since the 2019-2020 only just got started a few weeks ago
    yearList = []
    yearList.extend(range(1974,2021))

    # I'm using threads so it wont take double the time. They can scrape concurrently
    totalStatsThread = threading.Thread(target=totalStats_Scrape,args=(yearList,))
    per100StatsThread = threading.Thread(target=per100Stats_Scrape,args=(yearList,))
    totalStatsThread.start()
    per100StatsThread.start()

main()
