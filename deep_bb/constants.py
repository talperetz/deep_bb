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
PROCESSED_QNA_PATH = "../data/processed_data/bb_qna_list.pickle"
CHAT_PROCESSED_SENTENCES_PATH = "../data/processed_data/bb_sentences.pickle"
PROCESSED_QUOTES_PATH = "../data/processed_data/bb_quotes.txt"
PROCESSED_SPEECHES_PATHS = ["../data/raw_data/un_speech_2012.txt",
                            "../data/raw_data/un_speech_2013.txt",
                            "../data/raw_data/un_speech_2015.txt",
                            "../data/raw_data/un_speech_2016.txt",
                            "../data/raw_data/un_speech_2017.txt"]
SPEECH_PROCESSED_SENTENCES_PATH = "../data/processed_data/bb_speech_sentences.pickle"
INFERSENT_ALL_NLI_PATH = "../InferSent/encoder/infersent.allnli.pickle"
INFERSENT_GLOVE_PATH = '../InferSent/dataset/GloVe/glove.840B.300d.txt'
GENERAL_RESPONSES = ["sorry, I must consult with Sarah about it",
                     "while we speak Iran is paving it's path to nuclear weapons",
                     "I always lose the election in the polls, and I always win it on election day.",
                     "Some will criticize me no matter what I do.",
                     "I'm not naturally manipulative.",
                     "I've been right more than I've been wrong.",
                     "Populism is dangerous.",
                     "The State of Israel can be proud of what we're doing."
                     ]

# models

TWEETS_MODEL_PATH = '../models/tweets_markov_chains.pickle'
SPEECH_MODELS_PATH = '../models/speech_markov_chains.pickle'
CHAT_INFERSENT_MODEL_PATH = '../models/chat_infersent.pickle'
SPEECH_INFERSENT_MODEL_PATH = '../models/speech_infersent.pickle'
CHAT_EMBEDDED_SENTENCES_MATRIX_PATH = '../models/embedded_sentences_matrix.pickle'
SPEECH_EMBEDDED_SENTENCES_MATRIX_PATH = '../models/speech_embedded_sentences_matrix.pickle'
GENERAL_MODEL_PATH = '../models/general_responder.pickle'
LDA_CLUSTERS_PATH = '../models/lda_clusters.pickle'
SPEECH_MODEL_PATH = '../models/speech_mcc.pickle'


# params
LDA_N_PASSES = 240
LDA_N_TOPICS = 7
SPEECH_N_TOPICS = 3
LDA_TOPICS_MAP = {'intro':2, 'main':[3,5,6], 'continue':1, 'end':4}
MAX_TWEET_LENGTH = 140
SIMILARITY_THRESHOLD = 0.4
CHATTER_CONFIDENCE_THRESHOLD = 0.7

