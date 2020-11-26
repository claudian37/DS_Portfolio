import pandas as pd
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from wordcloud import WordCloud
import string
import matplotlib.pyplot as plt

import bitly_api
from utils.credentials import bitly_auth_keys

class TextProcessor(object):
	def __init__(self):
		pass

	def clean_text(self, article):
		if (article is None) or (pd.isna(article)):
			return None

		# Tokenize words in article
		tokens = word_tokenize(article)
		tokens_flattened = [t.strip() for t in tokens]

		# Return only characters
		tokens_chars = [t.lower() for t in tokens_flattened if t.isalpha()]

		# Remove stop words
		stop_words = list(set(stopwords.words('english')))
		[stop_words.append(x) for x in ['said', 'says', 'say']]
		cleaned_tokens = [t for t in tokens_chars if t not in stop_words]
		cleaned_tokens_str = " ".join(cleaned_tokens).strip()

		return cleaned_tokens_str

	def get_word_token_frequencies(self, cleaned_text, n_tokens=5):
		if not isinstance(cleaned_text, str):
			return None
		else:
			cleaned_text_tokens = cleaned_text.split()

		# Calculate frequency of each token
		fdist_tokens = FreqDist(cleaned_text_tokens)
		fdist_tokens_sorted = {k: v for k, v in sorted(fdist_tokens.items(), key=lambda x: x[1], reverse=True)[:n_tokens]}

		return fdist_tokens_sorted

	def plot_word_cloud(self, cleaned_text, fdist_tokens, path_save=None):
		cleaned_text_str = " ".join(str(t) for t in cleaned_text)

		# Make word cloud
		word_cloud = WordCloud().generate(cleaned_text_str)
		wc = word_cloud.generate_from_frequencies(fdist_tokens)

		fig = plt.figure(figsize=(12,12))
		plt.imshow(wc)
		plt.axis('off')
		plt.savefig(path_save, bbox_inches='tight')

	def shorten_url(self, url):
		bitly = bitly_api.Connection(access_token=bitly_auth_keys['auth_token'])
		url_shortened = bitly.shorten(url)

		return url_shortened