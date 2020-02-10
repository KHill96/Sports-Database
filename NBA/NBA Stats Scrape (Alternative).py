# Imports
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import pandas

def stats_Scrape(yearList = [], *args):
    fullList_totals = pandas.DataFrame()
    fullList_per100 = pandas.DataFrame()
    totals_URL = 'https://www.basketball-reference.com/leagues/NBA_{}_totals.html'
    per100__URL = 'https://www.basketball-reference.com/leagues/NBA_{}_per_poss.html'
    for year in yearList:
        totals_URL = totalsURL.format(year)
        per100_URL = per100URL.format(year)
        totals_HTML = urlopen(totals_URL)
        per100_HTML = urlopen(per100_URL)
        totals_Soup = bs(totalHTML,'html.parser')
        per100_Soup = bs(per100_Soup,'html.parser')
        totals_table = soup.find('table',{'id':'totals_stats'})
        per100_table = soup.find('table',{'id':'per_poss_stats'})
        totals_rows = totals_table.findAll('tr')
        per100_rows = per100_table.findAll('tr')
        totals_header = [th.getText() for th in total_rows[0].findAll('th')]
        per100_header = [th.getText() for th in per100_rows[0].findAll('th')]
        totals_header = total_header[1:]
        totals_rows = total_rows[1:]
        per100_header = total_header[1:]
        per100_rows = total_rows[1:]
        total_stats = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(totals_rows))]
        per100_stats = [[td.getText() for td in per100_rows[i].findAll('td') for i in range(len(per100_rows))]]
        total_stats = pandas.DataFrame(total_stats, columns=totals_header)
        total_stats.insert(0,'Season',year)
        per100_stats = pandas.DataFrame(per100_stats,columns=per100_header)
        per100stats.insert(0,'Season',year)
        fullList_totals = fullList_totals.append(total_stats,sort=False)
        fullList_per100 = fullList_per100.append(per100_stats,sort=False)
    fileName_totals = 'Total Stats.csv'
    fullList_totals.to_csv(fileName,index=False)
    fileName_totals = 'Per 100 Stats.csv'
    fullList_per100.to_csv(fileName,index=False)

def main():
    # Create a list of years from 1974 to 2019 since the 2019-2020 only just got started a few weeks ago
    yearList = []
    yearList.extend(range(1974,2020))
    stats_Scrape(yearList)

main()
