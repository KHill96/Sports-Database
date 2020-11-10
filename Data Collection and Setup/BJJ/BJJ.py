# Imports
from bs4 import BeautifulSoup as bs
from random import randint
from selenium import webdriver
import os
import pandas
import re
import string
import threading
import time

def scrape_table():
    print('[Competitor Info Table]{} Starting to scrape names and teams from BJJ Heroes\' \"Database\"'.format(time.strftime("%H:%M:%S",time.localtime())))
    driver = webdriver.Firefox()
    driver.get('https://www.bjjheroes.com/a-z-bjj-fighters-list')
    driver.minimize_window()
    html = driver.page_source.encode('utf-8')
    soup = bs (html,'html.parser')
    table = soup.find('table',{'id':'tablepress-8'})
    column_names = [th.text for th in table.find('thead').findAll('th')]
    rows = table.find('tbody').findAll('tr')
    info = []
    for i in range(len(rows)):
        data = []
        for td in rows[i].findAll('td'):
            data.append(td.text)
        info.append(data)
    driver.quit()
    competitor_coach_info = pandas.DataFrame(info,columns=column_names)
    competitor_coach_info = competitor_coach_info.replace(r'^\s*$', 'NULL', regex=True)
    # print(competitor_coach_info)
    print('[Competitor Info Table]{} Finsihed scraping names and teams from BJJ Heroes\' \"Database\"'.format(time.strftime("%H:%M:%S",time.localtime())))


def scrape_records():
    to_scrape = set(['https://www.bjjheroes.com/bjj-fighters/ryan-hall'
                    ,'https://www.bjjheroes.com/bjj-fighters/jones'
                    ,'https://www.bjjheroes.com/bjj-fighters/marcelo-garcia-fighter-profile'
                    ,'https://www.bjjheroes.com/bjj-fighters/ffion-davies'
                    ,'https://www.bjjheroes.com/bjj-fighters/mackenzie-dern'
                ])
    seen = set()
    print('[Competitor Record]{} Starting to scrape the Competitor Records'.format(time.strftime("%H:%M:%S",time.localtime())))
    total_frame = pandas.DataFrame()
    # Since python wants to hold my hand to make sure I don't iterate over a growing set, I made a second set to track what I've visited so far
    file_seen = open('seen.txt','a')
    driver = webdriver.Firefox()
    while seen != to_scrape:
        try:
            for url in to_scrape:
                file_to_scrape.write('{}\n'.format(url))
                # Since BJJ Heroes blocks a basic urlopen, I had to resort to using selenium.
                
                # If the url has already been scraped just pass this iteration
                if url in seen:
                    print('[Competitor Record]{} {} has already been scraped'.format(time.strftime("%H:%M:%S",time.localtime()),url))
                    pass

                # Otherwise build the dataframe and create 
                else:
                    try:  
                        # Avoiding an IP ban or whatever by sleeping for 1 to 3 minutes
                        print('[Competitor Record]{} Waiting to make the next request'.format(time.strftime("%H:%M:%S",time.localtime())))  
                        time.sleep(randint(30,180))
                        driver.get(url)
                        html = driver.page_source.encode('utf-8')

                        soup = bs(html,'html.parser')
                        # Obtain the name
                        name = soup.find('h1',{'itemprop':'name'}).text
                        print('[Competitor Record]{} Working on {}'.format(time.strftime("%H:%M:%S",time.localtime()),name))
                        # Obtain the table
                        record = soup.find('table',id=re.compile('^DataTables_Table_\d+'))
                        # Get the column names and add the name as the first column
                        column_names = [th.text for th in record.find('thead').findAll('th')]
                        # Get the rows of data
                        rows = record.find('tbody').findAll('tr')
                        stats = []
                        for i in range(len(rows)):
                            data = []
                            row_contents = rows[i].findAll('td')
                            for k in range(len(row_contents)): 
                                # If it's the first column (Opponent) and there's a link
                                if row_contents[k].find('a') and k == 0:
                                    data.append(row_contents[k].find('a').text)
                                    # Push link to array
                                    to_scrape.add('https://www.bjjheroes.com/bjj-fighters/{}'.format(row_contents[k].find('a').get('href')))
                                    
                                else:
                                    data.append(row_contents[k].text)
                            stats.append(data)

                        # Create the data frame
                        record_frame = pandas.DataFrame(stats, columns=column_names)
                        record_frame.insert(0,'Name',name)
                        total_frame.append(record_frame,sort=False)
                        print('[Competitor Record]{} Finished {}\'s record'.format(time.strftime("%H:%M:%S",time.localtime()),name))
                    except AttributeError:
                        print('[Competitor Record]{} {} had no record to scrape'.format(time.strftime("%H:%M:%S",time.localtime()),name))
                        continue
                    seen.add(url)
                    file_seen.write('{}\n'.format(url))

        
        except RuntimeError:
            continue
    driver.quit()
    file_seen.close()
    file_to_scrape.close*()
    total_frame.to_csv('BJJ Competitor Record.csv',index=False)
    print('[Competitor Record]{} Finished scraping the Competitor Records'.format(time.strftime("%H:%M:%S",time.localtime())))
    


def main():
    scrape_records()
    # scrape_table()


if __name__ == "__main__":
    main()