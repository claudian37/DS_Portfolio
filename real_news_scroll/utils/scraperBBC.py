import pandas as pd
import datetime as dt

from bs4 import BeautifulSoup
import requests

class ScraperBBC(object):
    def __init__(self):
        pass

    def scrape_site(self, url, element, attribute, news_page=False):
        """
        Function to scrape BBC website using BeautifulSoup. It takes the following functions
        - url (str): 'https://www.bbc.co.uk' for homepage; 
                      'https://www.bbc.co.uk/news' for news page.
        - element (str):element to find from scraped results.
        - attribute (str): attribute to find within element from scraped results.
        - news_page (boolean): True if scraping 'https://www.bbc.co.uk/news', else False.

        Returns scraped information in pandas DataFrame
        """ 
        response = requests.get(url)
        results = BeautifulSoup(response.text, 'html.parser')

        articles = results.find_all(element, {'class': attribute})
        all_articles = []

        for article in articles:
            dict_article = {}
            
            if news_page:
                headline = article.find('h3')
                if headline:
                    dict_article['headline'] = headline.text
                    
                link = article.find('a')
                if link:
                    if ('https://www.bbc.co.uk' in link['href']):
                        dict_article['link'] = link['href']
                    else:
                        dict_article['link'] = 'https://www.bbc.co.uk' + link['href']
                    
                summary = article.find('p')
                if summary:
                    dict_article['summary'] = summary.text
            
            else:
                headline = article.find('span')
                if headline:
                    dict_article['headline'] = headline.text
            
                link = article['href']
                if link:
                    dict_article['link'] = link
            
            dict_article['updated_time'] = dt.datetime.now().strftime('%Y-%m-%d %H:%m')

            if ('/live/' not in dict_article.get('link')) and ('news' in dict_article.get('link')):
                all_articles.append(dict_article)

        df = pd.DataFrame(all_articles)

        return df

    def parse_article(self, url, element):
        response = requests.get(url)
        results = BeautifulSoup(response.text, 'lxml')
        paragraphs = results.find(element)

        try:
            article = [p.text for p in paragraphs if (p.text != '') and ('image' not in p.text) and ('media caption' not in p.text)]
            article = article[1:-2] # Exclude title at the start, and "related topics" at the end 
            article = " ".join(article)
        except:
            article = None

        return article

