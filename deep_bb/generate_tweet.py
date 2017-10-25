#!/usr/bin/env python

"""
:Date: 10/25/17
:TL;DR:
:Abstract:
:Problem:
:Proposed Solution:
"""

from abc import ABCMeta, abstractmethod
import markovify
import pickle
from deep_bb import constants

__author__ = "Tal Peretz"
__copyright__ = "Copyright 2017"
__maintainer__ = "Tal Peretz"
__email__ = "talp@panorays.com"
__status__ = "Development"


class TweetGenerator:
    __metaclass__ = ABCMeta
    model = None

    @abstractmethod
    def preprocess(self, text):
        pass

    @abstractmethod
    def generate_tweet(self):
        pass


class MccTweetGenerator(TweetGenerator):

    def preprocess(self, text):
        mc_model = markovify.Text(text, state_size=2)
        with open(constants.TWEETS_MODEL_PATH, 'wb') as f:
            pickle.dump(mc_model, f)
        return self

    def generate_sentence(self, mc_model):
            s = None
            while not s:
                s = mc_model.make_short_sentence(max_chars=120, min_chars=4)
            return s

    def generate_tweet(self):
        with open(constants.TWEETS_MODEL_PATH, 'rb') as f:
            mc_model = pickle.load(f)
        output = self.generate_sentence(mc_model)
        return output


if __name__ == '__main__':
    with open(constants.CORPUS_PATH, 'r') as corpus:
        text = corpus.read().lower()

    mcc_speech_generator = MccTweetGenerator().preprocess(text)
    print(mcc_speech_generator.generate_tweet())
