from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import pandas
import string
def main():
    # Create a list for the data frames
    frames =[]

    # The player index uses the players last initial as the index
    # There's never been a player with a last name starting with x so I just got rid of it to avoid any errors
    playerStartingLetters = list(string.ascii_lowercase)
    playerStartingLetters.pop(23)

    # Go through each letters index and get the player information
    for letter in playerStartingLetters:

        # Create the link and start scraping
        link = 'https://www.basketball-reference.com/players/{}/'.format(letter)
        html = urlopen(link)
        soup = bs(html, 'html.parser')

        # Get the column names
        colRow = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
        # Skip the first row
        rows = soup.findAll('tr')[1:]
        # Get their info and put it into the frame
        info = pandas.DataFrame([[td.getText() for td in rows[i].findAll(['td','th'])]for i in range(len(rows))],columns=colRow)
        # add the frame to the list
        frames.append(info)

    # Put the frames together
    pandas.concat(frames).to_csv('Players.csv',index=False)
    print("Got all NBA Players")
main()
