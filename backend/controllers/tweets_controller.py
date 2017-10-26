from controllers.Controller import Controller
from deep_bb import constants
from deep_bb.generate_tweet import MccTweetGenerator
from utils import tweeter_utils
import os

DEEP_BB_PREFIX_PATH = '../deep_bb/'


class TweetController(Controller):
    def __init__(self):
        Controller.__init__(self)
        self._api = tweeter_utils.TweeterUtils()
        os.chdir(DEEP_BB_PREFIX_PATH)
        with open(constants.CORPUS_PATH, 'r') as corpus:
            text = corpus.read().lower()
        self.mcc_tweets_generator = MccTweetGenerator().preprocess([text])

    def _generate_random_tweet(self):
        return self.mcc_tweets_generator.generate_tweet()

    def _post_tweet(self):
        msg = self._api.tweet(self._generate_random_tweet())
        return msg
