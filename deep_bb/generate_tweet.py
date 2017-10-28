#!/usr/bin/env python

"""
:Date: 10/25/17
:TL;DR: deep_bb tweet generator component
:Abstract: DataHack 2017 - 2 days hackaton
:Problem: given a small amount of sentences and a smaller amount of q&a generate bb typical tweet
:Proposed Solution: markov chains with POS tagging (after a failed attempt with word-RNN)
"""


import markovify
import pickle
from deep_bb import constants
from deep_bb.abstracts import TweetGenerator
from deep_bb.utils import POSifiedText
import re

__author__ = "Tal Peretz"
__copyright__ = "Copyright 2017"
__maintainer__ = "Tal Peretz"
__email__ = "talp@panorays.com"
__status__ = "Development"


class MccTweetGenerator(TweetGenerator):

    def preprocess(self, texts, weights=None):
        weights = [1 for _ in texts] if weights is None else weights
        mc_models = []
        for text in texts:
            mc_models.append(markovify.Text(text, state_size=3))
        combined_model = markovify.combine(mc_models, weights)
        # mc_model = POSifiedText(text, state_size=3)
        with open(constants.TWEETS_MODEL_PATH, 'wb') as f:
            pickle.dump(combined_model, f)
        return self

    def generate_sentence(self, mc_model):
            s = None
            while not s or len(s) > constants.MAX_TWEET_LENGTH:
                s = mc_model.make_sentence()
            return s

    def generate_tweet(self):
        with open(constants.TWEETS_MODEL_PATH, 'rb') as f:
            mc_model = pickle.load(f)
        output = self.generate_sentence(mc_model)
        blank_with_punct = r"\s+[,.!?']+"

        def rep(m):
            return m.group(0).replace(r' ', '')
        corrected_output = re.sub(blank_with_punct, rep, output)
        return corrected_output


if __name__ == '__main__':
    # usage example:

    with open(constants.PROCESSED_TWEETS_PATH, 'r') as corpus:
        tweets_text = re.sub(pattern='\n+', repl='\n', string=corpus.read().lower())

    with open(constants.PROCESSED_QUOTES_PATH, 'r') as corpus:
        quotes_text = re.sub(pattern='\n+', repl='\n', string=corpus.read().lower())

    with open(constants.PROCESSED_FB_POSTS_PATH, 'r') as corpus:
        fb_text = re.sub(pattern='.', repl='.\n',string=re.sub(pattern='\n+', repl='\n', string=corpus.read().lower()))

    mcc_speech_generator = MccTweetGenerator().preprocess([tweets_text, fb_text, quotes_text], weights=[0.4, 2, 1])
    print(mcc_speech_generator.generate_tweet())
