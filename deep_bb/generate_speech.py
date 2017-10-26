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
import spacy
import pickle
import constants
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
    def preprocess(self, text):
        pass

    @abstractmethod
    def generate_speech(self, n_sentences=50):
        pass


class POSifiedText(markovify.Text):
    nlp = spacy.load("en")

    def word_split(self, sentence):
        sentence = sentence.decode('utf-8')
        return ["::".join((word.orth_, word.pos_)) for word in self.nlp(sentence)]

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


class MccSpeechGenerator(TweetGenerator):

    def preprocess(self, text):
        # mc_model = markovify.Text(text, state_size=3)
        mc_model = POSifiedText(text, state_size=2)
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
        blank_with_punct = r"\s+[,.!?']+"

        def rep(m):
            return m.group(0).replace(r' ', '')

        corrected_output = [re.sub(blank_with_punct, rep, sentence) for sentence in output]
        return '\n'.join(corrected_output)


if __name__ == '__main__':
    with open(constants.CORPUS_PATH, 'r') as corpus:
        text = corpus.read().lower()

    mcc_speech_generator = MccSpeechGenerator().preprocess(text)
    print(mcc_speech_generator.generate_speech())
