# Sports-Database
As a way of learning more about building and managing a database I decided to make my own using sports using boxing, mixed martial arts, and basketball to start. 

# How I collected the data
I decide to use web scraping as a way to get the data. It made more sense than manually going in and doing data entry for so many fighters.

## Boxing
For boxers and MMA fighters some issues came when trying to find their information and fight history. Some fighters like Manny Pacquiao and Muhammad Ali have separate pages for their boxing careers which is easy to miss if your collecting the links rather quickly. Originally, I put their information, record, and fight history into separate files making 3 for each fighter in the list. Considering I have over 100 fighters in the list this became a huch issue in regards to space. I decided to just scrape the tables and put the results into a txt file. I'm still inputting their fight history into the excel sheet to export as a csv but their information is already in the workbook. As time goes on I'll update the fight history table to hold the fighters I've collected.
This was really my first experience using python as a tool like this so in my opinion the code is rather clunky.

## NBA
This was significantly easier because I used basketball-reference.com and this site beautifully simply changes the extensions and has source code which makes it extremely easy to scrape. 
