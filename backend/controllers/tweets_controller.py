import os
import re
import traceback

from controllers.Controller import Controller
from utils import tweeter_utils

from deep_bb import constants
from deep_bb.generate_tweet import MccTweetGenerator

DEEP_BB_PREFIX_PATH = '../deep_bb/'


class TweetController(Controller):
    def __init__(self):
        Controller.__init__(self)
        self._api = tweeter_utils.TweeterUtils()
        os.chdir(DEEP_BB_PREFIX_PATH)

        with open(constants.PROCESSED_TWEETS_PATH, 'r') as corpus:
            tweets_text = re.sub(pattern='\n+', repl='\n', string=corpus.read().lower())

        with open(constants.PROCESSED_QUOTES_PATH, 'r') as corpus:
            quotes_text = re.sub(pattern='\n+', repl='\n', string=corpus.read().lower())

        with open(constants.PROCESSED_FB_POSTS_PATH, 'r') as corpus:
            fb_text = re.sub(pattern='.', repl='.\n',
                             string=re.sub(pattern='\n+', repl='\n', string=corpus.read().lower()))
            self.mcc_tweets_generator = MccTweetGenerator().preprocess([tweets_text, fb_text, quotes_text],
                                                                       weights=[0.4, 2, 1])
    def _generate_random_tweet(self):
        return self.mcc_tweets_generator.generate_tweet()

    def _post_tweet(self):
        is_tweet_sent = False
        while not is_tweet_sent:
            try:
                print 'generating tweet'
                msg = self._api.tweet(self._generate_random_tweet())
                self._api.like(msg.id)
                is_tweet_sent = True
                return msg
            except:
                traceback.format_exc()
