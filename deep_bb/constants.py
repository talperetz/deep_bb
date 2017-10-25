#!/usr/bin/env python

"""
:Date: 10/25/17
:TL;DR:
:Abstract:
:Problem:
:Proposed Solution:
"""

__author__ = "Tal Peretz"
__copyright__ = "Copyright 2017"
__maintainer__ = "Tal Peretz"
__email__ = "talp@panorays.com"
__status__ = "Development"

# data

SPEECHES_PATH = '../data/raw_data/'
CORPUS_PATH = "../data/processed_data/un_speeches.txt"
PREPROCESSED_FB_POSTS_PATH = [r'../data/raw_data/datahack_knesset_fb_posts.csv/Sheet1.csv',
                              r'../data/raw_data/datahack_knesset_fb_posts.csv/Sheet2-Table 1.csv']
PROCESSED_FB_POSTS_PATH = "../data/processed_data/bb_fb_posts.txt"
PROCESSED_TWEETS_PATH = "../data/processed_data/bb_tweets.txt"

# models
TWEETS_MODEL_PATH = '../models/tweets_markov_chains.pickle'
SPEECH_MODEL_PATH = '../models/speech_markov_chains.pickle'
CHAT_MODEL_PATH = '../models/chat_markov_chains/'

QUERY_MATCH_CONFIDENCE_THRESHOLD = 0.5

