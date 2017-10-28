#!/usr/bin/env python

"""
:Date: 10/28/17
:TL;DR: module for containing abstract classes
"""

from abc import ABCMeta, abstractmethod

__author__ = "Tal Peretz"
__copyright__ = "Copyright 2017"
__maintainer__ = "Tal Peretz"
__email__ = "talp@panorays.com"
__status__ = "Development"


class Responder:
    __metaclass__ = ABCMeta

    @abstractmethod
    def reply(self, query):
        pass


class SpeechGenerator:
    __metaclass__ = ABCMeta
    model = None

    @abstractmethod
    def preprocess(self, text):
        pass

    @abstractmethod
    def generate_speech(self, n_sentences=50):
        pass


class TweetGenerator:
    __metaclass__ = ABCMeta
    model = None

    @abstractmethod
    def preprocess(self, texts, weights=None):
        pass

    @abstractmethod
    def generate_tweet(self):
        pass