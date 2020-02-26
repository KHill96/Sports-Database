# TODO: Try to build the dataframe with Khabib and Floyd. See if there isn't a way to have just one data frame
# TODO: split up the crossover fighters. Boxing to MMA has the boxing record come up first, MMA to boxing is the other way around

from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import json
import pandas

# Because wikipedia sucks I have to make two data frames:
    # One for MMA Fighters
    # One for Boxers
# There are some fighters who competed in both sports professionally but wikipedia will put their "main" sport as the first table
# So James Toney has his boxing record come up first instead of his MMA record

# Global
boxerSet = set()
mmaSet = set()
crossoverSet = set()
df = pandas.DataFrame()
wikiTemplate = 'https://en.wikipedia.org{}'

def buildMMASet():
    # MMA Set
    with open('MMA_Fighters.json') as MMA_JSON:
        data = json.load(MMA_JSON)
    for link in data["mmaFighterLinks"]:
        mmaSet.add(link)

    # Crawl links
    # print(mmaSet.__contains__('https://en.wikipedia.org/wiki/Khabib_Nurmagomedov'))
    seen = set()
    # Playing dangerously
    while seen != mmaSet:
        try:
            for link in mmaSet:
                if seen.__contains__(link):
                    mmaSet.add(link)
                    pass
                else:
                    seen.add(link)
                    print(link)
                    html = urlopen(link)
                    soup = bs(html,'html.parser')
                    recordTable = soup.findAll('table',{'class':'wikitable'})[1]
                    rows = recordTable.findAll('tr')
                    tds = [row.findAll('td') for row in rows]
                    for i in range(1,len(rows)):
                        try:
                            linkRetrieved = tds[i][2].find('a',href=True)
                            mmaSet.add(wikiTemplate.format(linkRetrieved['href']))
                        except TypeError:
                            pass
                        except IndexError:
                            continue
        except RuntimeError:
            continue
    with open('test1.txt','w') as testFile:
        for link in mmaSet:
            testFile.write(link)
            testFile.write('\n')
        
    
def RecordScrapeMMA(link):

    soup = bs(urlopen(link),'html.parser')
    recordTable = soup.findAll('table',{'class':'wikitable'})[1]
    rows = recordTable.findAll('th')
    print(rows[1].text)
# FOR BOXERS!!!!!!
    # test = rows[1].findAll('td')[3].findAll('a')[1]


# Main
def main():
    with open('CrossoverFighters.json') as crossoverJSON:
        data = json.load(crossoverJSON)
    for link in data["BoxingToMMA"]:
        crossoverSet.add(link)
    buildMMASet()
main()