import tweepy

CUSTOMER_API_KEY = 'EXi5CtXtxQoqTIIsSF7FgRE8T'
CUSTOMER_SECRET = 'JYUw1bVU7KojCQquVTloZBmd1d8OSkjXDbyQo9IDmmlebYr2AV'

ACCESS_TOKEN = '920207242376499200-YKsUav4wZ00bCJXJAZbFCn8NtNgtWVu'
ACCESS_TOKEN_SECRET = '069cKsQRI1LJ5iBVYF0nVBgsabysv4P8LbhZWSeqfgiDF'


class TweeterUtils:
    def __init__(self):
        self._api = self.get_api()

    def get_api(self):
        auth = tweepy.OAuthHandler(CUSTOMER_API_KEY, CUSTOMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        return tweepy.API(auth)

    def tweet(self, msg):
        status = self._api.update_status(msg)
        return status

    def like(self, tweet_id):
        try:
            self._api.create_favorite(tweet_id)
        except:
            pass
