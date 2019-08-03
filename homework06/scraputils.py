import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []

    authors = parser.select('.subtext > .hnuser')
    comments = [i.text.split()[0]
                for i in parser.select('.subtext > a:nth-child(6)')]
    points = [i.text.split()[0] for i in parser.select('.subtext > .score')]
    titles = parser.select('.athing > .title > a')
    urls = parser.select('.athing .sitestr')

    for aut, cmnt, pnt, ttl, url in zip(authors, comments, points, titles, urls):
        news_list.append({
            'author': aut.text,
            'comments': int(cmnt) if cmnt.isdigit() else 0,
            'points': int(pnt),
            'title': ttl.text,
            'url': url.text
        })

    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    return parser.select('.morelink[rel=next]')[0].get('href')


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news
