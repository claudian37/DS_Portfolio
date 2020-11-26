import tweepy
from utils.credentials import twitter_auth_keys

class TwitterManager(object):
	def __init__(self):
		self._consumer_key = twitter_auth_keys['consumer_key']
		self._consumer_secret = twitter_auth_keys['consumer_secret']
		self._access_token = twitter_auth_keys['access_token']
		self._access_token_secret = twitter_auth_keys['access_token_secret']
		self.api = None

	def authenticate(self):
		auth = tweepy.OAuthHandler(self._consumer_key, self._consumer_secret)
		auth.set_access_token(self._access_token, self._access_token_secret)
		try:
			self.api = tweepy.API(auth)
			print('Authentication complete')
		except:
			Exception
		return self.api

	def post_tweet(self, message):
		assert self.api is not None, "Authentication needed"
		status = self.api.update_status(status=message)
		print(f'Successfully tweeted: "{message}"')
