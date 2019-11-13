# Libraries imported/used
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import pandas

def main():
    # Links to the types of stats I want to scrape
    links = ['https://www.basketball-reference.com/leagues/NBA_{}_totals.html',
            'https://www.basketball-reference.com/leagues/NBA_{}_per_game.html'
            ,'https://www.basketball-reference.com/leagues/NBA_{}_per_minute.html'
            ,'https://www.basketball-reference.com/leagues/NBA_{}_per_poss.html']

    # Create a list of years from 1974 to 2019 since the 2019-2020 only just got started a few weeks ago
    yearList = []
    yearList.extend(range(1974,2020))
    for year in yearList:
        for link in links:
            #Replace the {} characters with the year
            link = link.format(year)

            # Get the html to scrape
            html = urlopen(link)
            soup = bs(html,'html.parser')

            #Name the columns of the csv
            headerRow = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
            headerRow = headerRow[1:]
            # Get the data using findAll
            rows = soup.findAll('tr')[1:]
            stats = [[td.getText() for td in rows[i].findAll('td')]for i in range(len(rows))]
            stats = pandas.DataFrame(stats,columns= headerRow)
            fileName = link[link.rfind('NBA'):].replace('_',' ')
            # Cleanup the file name and create the csv
            fileName = fileName.replace('.html','')
            fileName = fileName +'.csv'
            stats.to_csv(fileName,index=False)

main()
