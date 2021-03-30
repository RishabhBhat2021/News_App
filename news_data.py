from bs4 import BeautifulSoup

import requests

class NewsData:
    headline_site = "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtVnVHZ0pKVGlnQVAB?hl=en-IN&gl=IN&ceid=IN%3Aen"
    site = "https://news.google.com"

    def __init__(self):
        self.request = requests.get(self.headline_site)
        self.content = self.request.text

        self.soup = BeautifulSoup(self.content, 'lxml')

        news_articles = self.soup.find_all('h3')

        self.news = {}

        for article in news_articles:
            headline = article.a.text
            link = article.a.attrs['href'].strip('.')
            article_link = f"{self.site}{link}"

            self.news[headline] = article_link

    def get_headlines(self):
        return self.news.keys()

    def get_link(self, headline):
        return self.news[headline]

class NewsDetail:
    def __init__(self, link):
        self.request = requests.get(link)
        self.content = self.request.text

        self.soup = BeautifulSoup(self.content, 'lxml')

        self.main_heading = ""
        self.sub_heading = ""
        self.paragraphs = ""

        main_heading_list = self.soup.find_all('h1')
        for head in main_heading_list:
            self.main_heading = self.main_heading + head.text

        sub_heading_list = self.soup.find_all('h2')
        for heading in sub_heading_list:
            self.sub_heading = self.sub_heading + heading.text + "\n"

        paragraphs_list = self.soup.find_all('p')
        for paragraph in paragraphs_list:
            self.paragraphs = self.paragraphs + paragraph.text + "\n"