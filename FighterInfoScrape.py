import urllib2
from urllib2 import urlopen
import bs4 as bs

file = open('FightersToScrape.txt')
links = file.readlines()
for link in links:
    # Replace Link for each fighter
    url = link
    html = urllib2.urlopen(url).read()
    soup = bs.BeautifulSoup(html,'lxml')

    # Return every table with "wikitable" in it's classnames
    fighterTables = soup.find_all('table',{'class':'wikitable'})
    # Get the fighters name (as listed on Wikipedia)
    fighterName = soup.find('h1',{'id':'firstHeading'}).text
    fighterTables = (fighterTables[0],fighterTables[1])
    # print historyTableAttr[0].prettify()
    for table in fighterTables:
        # print(fighterName)
        if(fighterTables.index(table) == 0):
            str = ''
            for row in table.find_all('tr'):
                for cell in row.find_all('td'):
                    str = str + u"{}".format((((cell.text)).replace('\n','')))
                    str = str + ', '
                    str = str.replace(u'\u2013','-')
            # Encode to avoid errors
            str = str.encode('ascii', 'ignore').decode('ascii')
            str = str.replace(' ,' , ',')
            fileName = fighterName + ' Record.txt'
            with open(fileName,'w') as r:
                r.write(str)

        else:
            str = ''
            for row in table.find_all('tr'):
                for cell in row.find_all('td'):
                    str = str + u"{}".format((((cell.text)).replace('\n','')))
                    str = str + ', '
                    str = str.replace(u'\u2013','-')
            # Encode to avoid errors
            str = str.encode('ascii', 'ignore').decode('ascii')

            #Formatting
            str = str.replace(' Win,', '\nWin,')
            str = str.replace(' Loss', '\nLoss')
            str = str.replace(' Draw', '\nDraw')
            str = str.replace(',  ', ',')
            str = str.replace(', ', ',')
            str = str.replace(',,', ',')
            fileName = fighterName + '.txt'
            with open(fileName,'w') as r:
                r.write(str)
        # print(str)

    print (fighterName + ' data done')
