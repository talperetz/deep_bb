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
import spacy
from deep_bb import constants
import re

__author__ = "Tal Peretz"
__copyright__ = "Copyright 2017"
__maintainer__ = "Tal Peretz"
__email__ = "talp@panorays.com"
__status__ = "Development"


class TweetGenerator:
    __metaclass__ = ABCMeta
    model = None

    @abstractmethod
    def preprocess(self, texts, weights=None):
        pass

    @abstractmethod
    def generate_tweet(self):
        pass


class POSifiedText(markovify.Text):
    nlp = spacy.load("en")

    def word_split(self, sentence):
        sentence = sentence.decode('utf-8')
        return ["::".join((word.orth_, word.pos_)) for word in self.nlp(sentence)]

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


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
    with open(constants.PROCESSED_TWEETS_PATH, 'r') as corpus:
        tweets_text = re.sub(pattern='\n+', repl='\n', string=corpus.read().lower())

    with open(constants.PROCESSED_QUOTES_PATH, 'r') as corpus:
        quotes_text = re.sub(pattern='\n+', repl='\n', string=corpus.read().lower())

    with open(constants.PROCESSED_FB_POSTS_PATH, 'r') as corpus:
        fb_text = re.sub(pattern='.', repl='.\n',string=re.sub(pattern='\n+', repl='\n', string=corpus.read().lower()))
    # print text
    mcc_speech_generator = MccTweetGenerator().preprocess([tweets_text, fb_text, quotes_text], weights=[0.4, 2, 1])
    print(mcc_speech_generator.generate_tweet())
