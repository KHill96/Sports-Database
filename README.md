# PYTHON VERSION USED:
***Python 3.7***


# Sports-Database
As a way of learning more about building and managing a database I decided to make my own using sports using boxing, mixed martial arts, and basketball to start.

# How I collected the data
I decide to use web scraping as a way to get the data. It made more sense than manually going in and doing data entry for so many fighters.

## Boxing
For boxers and MMA fighters some issues came when trying to find their information and fight history. Some fighters like Manny Pacquiao and Muhammad Ali have separate pages for their boxing careers which is easy to miss if your collecting the links rather quickly. Originally, I put their information, record, and fight history into separate files making 3 for each fighter in the list. Considering I have over 100 fighters in the list this became a huch issue in regards to space. I decided to just scrape the tables and put the results into a txt file. I'm still inputting their fight history into the excel sheet to export as a csv but their information is already in the workbook. As time goes on I'll update the fight history table to hold the fighters I've collected.
This was really my first experience using python as a tool like this so in my opinion the code is rather clunky.

## Basketball , Football, and Baseball
This was significantly easier because the websites basketball-reference.com, pro-football-reference.com, and baseball-reference.com are all very simple to scrape. They do offer to download the tables as csv but as stated before this could be extremely time consuming to do for every individual year. The script I wrote for this is much cleaner than the one made for the fighters. It uses the pandas library to create a data frame and exports that to a csv

###### Basketball
Basketball stats are broken down the the categories per game, per 36 minutes, per 100 possessions, and totals. On basketball-reference, there is another tab for the advanced stats but I chose not to take those stats and learn how to calculate them myself. I pulled the stats for every season since 1974. For every season up to and including 1973 there are no stats per 100 possessions. Since I don't really have an interest going that far back 1974 seemed to be a good starting spot. I also didn't pull any stats for the current season since it's only started less than a month ago. I may pull the stats during the All Star break in early 2020 and then update them once the playoffs start.

###### Football


###### Baseball
