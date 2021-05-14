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
        return [url, 'Error', '', '', '']

    # Extract the page's html
    html = response.text

    # use one of the lines below, html.parser works on windows and lxml works on mac
    soup = BeautifulSoup(html, features='html.parser')
    # soup = BeautifulSoup(html, features='lxml')

    powered_by_headway = 'headwayapp.co' in html.lower()
    if powered_by_headway:
        changelog = soup.find('section', attrs={'id': 'changelog-list'}) is not None

        if changelog:
            list_posts = soup.find('section', attrs={'id': 'changelog-list'}).findChildren()[0].findChildren()
            list_posts = [x for x in list_posts if x.get('itemtype') == 'http://schema.org/BlogPosting']

            if len(list_posts) == 0:
                return [url, True, True, 'NoPosts', '']

            post1 = list_posts[0].find('time').get('datetime')  # 0 is the first post
            post2 = list_posts[-1].find('time').get('datetime')  # -1 is the last post

            date1 = datetime.fromisoformat(post1[:-1])
            date2 = datetime.fromisoformat(post2[:-1])

            if len(list_posts) == 1:
                return [url, True, True, date1, 'Only1Post']

            average_days_between_posts = str((date1 - date2) / (len(list_posts) - 1))
            return [url, True, True, date1, average_days_between_posts]
        else:
            return [url, True, False, '', '']
    else:
        return [url, False, '', '', '']


if __name__ == '__main__':
    print(scrape('changelog.clearhaus.com/'))
