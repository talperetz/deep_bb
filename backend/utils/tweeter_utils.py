import tweepy

CUSTOMER_API_KEY = 'o5zzr3iv6lpDmzzsQZrgjkjrW'
CUSTOMER_SECRET = 'PrKZdQ3rp3zR1u4uXl9tfIt4yV1MJ4rIN89tdmV60MsiHgpKiu'

ACCESS_TOKEN = '920207242376499200-phc1Ojhy9yRVtbdiWPxMfK2SUf0WJQz'
ACCESS_TOKEN_SECRET = 'ePEHRNCizCpFYxYHbc7scHo2HwbA12w1Po41JTEHaHZhj'


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
