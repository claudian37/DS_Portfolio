import datetime as dt
from utils.scraperBBC import ScraperBBC
from utils.textProcessor import TextProcessor
from utils.twitterManager import TwitterManager

n_headlines = 3

# Scrape headlines and articles
bbc_scraper = ScraperBBC()
df_bbc = bbc_scraper.scrape_site(url='https://www.bbc.co.uk/news', 
	                             element='div', 
	                             attribute='gs-c-promo',
	                             news_page=True)

df_bbc_filtered = df_bbc[:n_headlines].copy()
df_bbc_filtered['article'] = df_bbc_filtered['link'].apply(lambda x: bbc_scraper.parse_article(url=x, element='article'))

# Process scraped articles
tp = TextProcessor()
df_bbc_filtered['cleaned_text'] = df_bbc_filtered['article'].apply(lambda x: tp.clean_text(x))
df_bbc_filtered['cleaned_summary'] = df_bbc_filtered['summary'].apply(lambda x: tp.clean_text(x))
df_bbc_filtered['token_frequencies'] = df_bbc_filtered.apply(lambda x: tp.get_word_token_frequencies(x['cleaned_text'], n_tokens=5), axis=1)
df_bbc_filtered['url_short'] = df_bbc_filtered['link'].apply(lambda x: tp.shorten_url(x)['url'])

print(df_bbc_filtered.head())

# Post to twitter
tm = TwitterManager()
tm.authenticate()

headline = df_bbc_filtered['headline']
summary = df_bbc_filtered['summary']
url_shortened = df_bbc_filtered['url_short']
top_keywords = df_bbc_filtered['token_frequencies']

for i in range(n_headlines):
    message = f"[{dt.datetime.today().strftime('%Y-%m-%d %H:%M')}] BBC Top Headline ({str(i+1)} of {str(n_headlines)}): " + \
              f"{headline[i]}. {summary[i]} {url_shortened[i]} #{' #'.join(top_keywords[i].keys())}"
    print(len(message))
    try:
    	tm.post_tweet(message=message)
    except Exception as e:
        print(e)
        continue