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
import nltk
import pickle
import constants

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
    def generate_speech(self, n_sentences=50):
        pass


class MccSpeechGenerator(TweetGenerator):

    def preprocess(self, text):
        mc_model = markovify.Text(text, state_size=3)
        with open(constants.SPEECH_MODEL_PATH, 'wb') as f:
            pickle.dump(mc_model, f)
        return self

    def generate_intro(self):
        return ['ladies and gentlemen,']

    def generate_sentence(self, mc_model):
            s = None
            while not s:
                s = mc_model.make_sentence()
            return s

    def generate_speech(self, sentence_starter=None, n_sentences=15):
        with open(constants.SPEECH_MODEL_PATH, 'rb') as f:
            mc_model = pickle.load(f)
        output = list()
        intro = self.generate_intro()
        output.extend(intro)
        for i in range(n_sentences - len(intro)):
            output.append(self.generate_sentence(mc_model))
        return '\n'.join(output)


if __name__ == '__main__':
    with open(constants.CORPUS_PATH, 'r') as corpus:
        text = corpus.read().lower()

    mcc_speech_generator = MccSpeechGenerator().preprocess(text)
    print(mcc_speech_generator.generate_speech())
