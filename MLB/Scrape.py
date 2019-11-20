from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import pandas
import string

def main():
    years = []
    years.extend(range(2018,2020))
    links = ['http://www.espn.com/mlb/stats/pitching/_/year/{}/',
            'http://www.espn.com/mlb/stats/batting/_/year/{}/',
            'http://www.espn.com/mlb/stats/fielding/_/year/{}/']
    for link in links:
        for year in years:
            html = urlopen(link)
            soup = bs(html,'html.parser')
            table = soup.find('table',{'class':'tablehead'})
            rows = table.findAll('tr')[1:]
            headerRow = table.find('tr',{'class':'colhead'})
            headerRow = [th.getText() for th in headerRow]
            print(headerRow)
            stats = [[td.getText() for td in rows[i].findAll('td')]for i in range(len(rows))]


            stats = pandas.DataFrame(stats,columns= headerRow)
            if ('batting' in link):
                fileName = 'Batting {}'.format(year)
                print(fileName)
            elif ('fielding' in link):
                fileName = 'Fielding {}'.format(year)
                print(fileName)
            else :
                fileName = 'Pitching {}'.format(year)
                print(fileName)
            stats.to_csv(fileName,index=False)
main()


# Write a method for each position. Becuase espn is shitty
