import urllib2
import bs4 as bs

file = open('FightersToScrape.txt')
links = file.readlines()
for link in links:
    # Replace Link for each fighter, read it, and prep to scrape it
    url = link
    html = urllib2.urlopen(url).read()
    soup = bs.BeautifulSoup(html,'lxml')

    # Return every table with "wikitable" in it's classnames
    fighterTables = soup.find_all('table',{'class':'wikitable'})
    # Get the fighters name (as listed on Wikipedia)
    fighterName = soup.find('h1').text
    # For their record and fight history I only need to use the first two tables
    # Get the table holding their general information
    fighterInfoTable = soup.find('table',class_='infobox')
    # Get their name as listed on wikipedia
    del fighterTables[-1]
    # Get their general info
    str = ''
    for row in fighterInfoTable.find_all('tr'):
        for cell in row.find_all('td'):
            str = str + u"{}".format((((cell.text)).replace('\n','')))
            str = str + ', '
            str = str.replace(u'\u2013','-')
    # Encode to avoid errors
    str = str.encode('ascii', 'ignore').decode('ascii')
    str = str.replace(' ,' , ',')
    # Write the info to a txt file
    #Formatting
    str = str.replace(',Professional', '\nProfessional')
    str = str.replace(',  ', ',')
    str = str.replace(', ', ',')
    str = str.replace(',,', ',')

    # Go through the tables for their record and fight history
    for table in fighterTables:
        # print(fighterName)
        for row in table.find_all('tr'):
            for cell in row.find_all('td'):
                str = str + u"{}".format((((cell.text)).replace('\n','')))
                str = str + ', '
                str = str.replace(u'\u2013','-')
        # Encode to avoid errors
        str = str.encode('ascii', 'ignore').decode('ascii')
        str = str.replace(' ,' , ',')

    str = str.replace(',Professional', '\nProfessional')
    str = str.replace(' Win,', '\nWin,')
    str = str.replace(' Loss', '\nLoss')
    str = str.replace(' Draw', '\nDraw')
    str = str.replace('NC,','\nNC')
    str = str.replace ('\nDraws','Draws')
    str = str.replace(',  ', ',')
    str = str.replace(', ', ',')
    str = str.replace(',,', ',')
    fileName = fighterName + ' .txt'
    with open(fileName,'w') as r:
        r.write(str)

    # Let me know the fighter's info is collected
    print (fighterName + ' data done')

