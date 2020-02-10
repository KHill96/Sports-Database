# Imports
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import pandas
import time
from selenium import webdriver

# Function to scrape the team standings
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
    fileName = 'Standings.csv'
    fullList.to_csv(fileName,index=False)
    print(fullList)

def main():
    yearList = []
    yearList.extend(range(1974,2020))
    standingsScrape(yearList)
    
main()