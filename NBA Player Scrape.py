from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import pandas
import string

frames =[]
playerStartingLetters = list(string.ascii_lowercase)
playerStartingLetters.pop(23)
print(playerStartingLetters)
for letter in playerStartingLetters:
    link = 'https://www.basketball-reference.com/players/{}/'.format(letter)
    html = urlopen(link)
    soup = bs(html)
    colRow = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
    rows = soup.findAll('tr')[1:]
    info = pandas.DataFrame([[td.getText() for td in rows[i].findAll(['td','th'])]for i in range(len(rows))],columns=colRow)
    frames.append(info)
pandas.concat(frames).to_csv('Players.csv',index=False)
