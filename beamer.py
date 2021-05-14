import requests

from bs4 import BeautifulSoup

from datetime import datetime

requests.packages.urllib3.disable_warnings()


def scrape(url):
    print('u', end='')  # To show progress

    # cut off last two characters if the url ends with /*
    if url.endswith('/*'):
        url = url[:-2]

    # Get the webpage, creating a Response object.
    try:
        response = requests.get('http://' + url, timeout=5, verify=False)
    except:
        return [url, 'Error', '', '', '', '', '']

    # Extract the page's html
    html = response.text

    # use one of the lines below, html.parser works on windows and lxml works on mac
    soup = BeautifulSoup(html, features='html.parser')
    # soup = BeautifulSoup(html, features='lxml')

    powered_by_beamer = 'powered by beamer' in html.lower()
    if powered_by_beamer:
        change_log = soup.find('span', attrs={'class': 'catItemName'}) is not None

        if change_log:
            free_user = 'app.getbeamer.com' in url

            watermark = 'feed by' in html.lower()

            most_recent_post = soup.find('div', attrs={'class': 'featureDate'}).findChildren()[-1].text

            list_posts = soup.find('div', attrs={'id': 'firstResults'}).findChildren()
            list_posts = [x for x in list_posts if x.get('role') == 'listitem']

            post1 = list_posts[0].findChild().findChildren()[-1].text  # 0 is the first post
            post2 = list_posts[-1].findChild().findChildren()[-1].text  # -1 is the last post

            date1 = datetime.strptime(post1, '%B %d, %Y')
            date2 = datetime.strptime(post2, '%B %d, %Y')

            average_days_between_posts = (date1 - date2).days / (len(list_posts) - 1)

            return [url, True, True, free_user, watermark, most_recent_post, average_days_between_posts]
        else:
            return [url, True, False, '', '', '', '']
    else:
        return [url, False, '', '', '', '', '']


if __name__ == '__main__':
    print(scrape('updates.convertflow.com'))
