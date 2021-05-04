import scrapy

import requests

from bs4 import BeautifulSoup

from datetime import datetime

def scrape(row):

    url = "http://" + row
    # if url ends with /* then cut off last two digits to prevent website access problems 
    if url.endswith('/*'):
        url = url[:-2]
    print("u", end="")
    # Getting the webpage, creating a Response object.
    try:
        response = requests.get(url, timeout = 5)
    except Exception as e:
        return[row, 'Error', "", "", "", "",""]

    # Extracting the source code of the page.
    data = response.text
    soup = BeautifulSoup(data, features="lxml")

    if 'powered by beamer' in data.lower():

        change_log = soup.find('span', attrs={'class':'catItemName'}) is not None

        if change_log: 

            free_user = 'app.getbeamer.com' in url
            
            water_mark = 'feed by' in data.lower()
            
            most_recent_post = soup.find('div', attrs={'class':'featureDate'}).findChildren()[-1].text

            # change 'class' to 'id' because it is div id not div class  
            list_posts = soup.find('div', attrs={'id':'firstResults'}).findChildren()
            list_posts = [x for x in list_posts if x.get('role') == 'listitem']

            # 0 is the first post
            post1 = list_posts[0].findChild().findChildren()[-1].text
            # -1 is the last post 
            post2 = list_posts[-1].findChild().findChildren()[-1].text
            
            date1 = datetime.strptime(post1, '%B %d, %Y')

            date2 = datetime.strptime(post2, '%B %d, %Y')

            average_days_between_posts = (date1 - date2).days/(len(list_posts) - 1)

            return [row, True, True, free_user, water_mark, most_recent_post, average_days_between_posts]
        else:
            return [row, True, False, "", "", "", ""]
    else:
        return [row, False, "", "", "", "", ""]


if __name__ == '__main__':
    print(scrape("updates.convertflow.com"))