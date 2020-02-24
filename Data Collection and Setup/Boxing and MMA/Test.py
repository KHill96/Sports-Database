# TODO: Trim the list
# TODO: Try to build the dataframe with Khabib and Floyd. See if there isn't a way to have just one data frame
# TEST ON A DUMMY LAPTOP (Macbook, forget the speed)
# IDEA: 6 degrees of *Insert Name*
#ISSUE: Guys like James Toney and Conor McGregor did both Boxing and MMA.
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import json

# Because wikipedia sucks I have to make two data frames:
    # One for MMA Fighters
    # One for Boxers

# Build the set of links
def buildBoxerSet():
    with open('Boxers.json') as f:
        data = json.load(f)
   
    # Create a set to hold links that we already scraped
    boxerSet = set()
    for link in data["boxerLinks"]:
        boxerSet.add(link)
    boxerSet_Crawled = set()
    # while the set doesn't have all the links from the JSON
    for link in boxerSet:
        # If the link is in the set pass to the next
        if link not in boxerSet_Crawled:
            html = urlopen(link)
            soup = bs(html,'html.parser')
            table = soup.findAll('table',{'class':'wikitable'})[1]
            rows = table.findAll('tr')
            tds = [a for a in rows.findAll('td').find('a')]
            print(td)
        # Else Scrape it for the thinks
    # Export the final file(s)

# MMA Fighter Scrape
def buildMMAFighterSet():
    # Beautiful Soup Drill
    wikiTemplate = 'https://en.wikipedia.org{}'
    with open('MMA_Fighters.json') as f:
        data = json.load(f)
    mmaSet = set()
    for link in data['mmaFighterLinks']:
        mmaSet.add(link)
    html = urlopen(url)
    soup = bs(html,'html.parser')
    table = soup.findAll('table',{'class':'wikitable'})[1]
    rows = table.findAll('tr')
    tds = [row.findAll('td') for row in rows]
    # Change the row not the column
    test = []
    for i in range(1,len(rows)):
        test.append(tds[i][2].find('a',href=True))
    print(wikiTemplate.format(test[0]['href']))
    
# def boxerScrape():

# Main
def main():
    MMA_FighterScrape()
main()