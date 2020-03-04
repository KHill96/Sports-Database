from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup as bs
import json
import pandas

passingLink = 'https://www.pro-football-reference.com/years/{}/passing.htm'
rushingLink = 'https://www.pro-football-reference.com/years/{}/rushing.htm'




def passingScrape (yearList = [], *args):
    passingStats = pandas.DataFrame()
    for year in yearList:
        copyLink = passingLink.format(year)
        soup = bs(urlopen(copyLink),'html.parser')
        table = soup.find('table',{'id':'passing'})
        header = [th.text for th in table.find('thead').findAll('th')].remove('Rk')
        rows = table.findAll('tr')[1:]
        passingStatsArr = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]
        tempFrame = pandas.DataFrame(passingStatsArr,columns=header)
        tempFrame.insert(0,'Season',year,False)
        passingStats = passingStats.append(tempFrame,sort=False)
        print('Passing for {} done'.format(year))
    passingStats.to_csv('Passing.csv',index=False)

# def scrapeHelper(yearRange, DataFrame (orginal), link):

def main():
    # Thread for passing
    passingScrape(range(1974,2020))
    # Thread for Rushing
    # rushingScrape()
    #...

if __name__ == "__main__":
    main()