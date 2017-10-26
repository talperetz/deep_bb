from controllers.Controller import Controller
from deep_bb import constants
from deep_bb.generate_tweet import MccTweetGenerator
from utils import tweeter_utils
import os
import pyttsx

DEEP_BB_PREFIX_PATH = '../deep_bb/'


class TweetController(Controller):
    def __init__(self):
        Controller.__init__(self)
        self._api = tweeter_utils.TweeterUtils()
        os.chdir(DEEP_BB_PREFIX_PATH)
        with open(constants.PROCESSED_TWEETS_PATH, 'r') as corpus:
            text = corpus.read().lower()
        self.mcc_tweets_generator = MccTweetGenerator().preprocess([text])

    def _generate_random_tweet(self):
        # engine = pyttsx.init()
        return self.mcc_tweets_generator.generate_tweet()

    def _post_tweet(self):
        is_tweet_sent = False
        while is_tweet_sent:
            try:
                msg = self._api.tweet(self._generate_random_tweet())
                is_tweet_sent = True
                return msg
            except:
                pass
