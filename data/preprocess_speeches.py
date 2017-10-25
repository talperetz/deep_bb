#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Date: 9/20/17
:TL;DR:
:Abstract:
:Problem:
:Proposed Solution:
"""

import os
import nltk
from deep_bb import constants
import string
import pandas as pd

__author__ = "Tal Peretz"
__copyright__ = "Copyright 2017"
__maintainer__ = "Tal Peretz"
__email__ = "talp@panorays.com"
__status__ = "Development"


def merge_files(in_paths, out_path):
    with open(out_path, 'w') as out_file:
        for path in in_paths:
            with open(path, 'r') as in_file:
                for l in in_file:
                    out_file.write(l)


def merge_speeches():
    speeches_paths = [constants.SPEECHES_PATH + '{}'.format(filename) for filename in
                      os.listdir(constants.SPEECHES_PATH)]
    merge_files(speeches_paths, constants.CORPUS_PATH)


def filter_english(sentences):
    english_sentences = []
    words = set(nltk.corpus.words.words())
    printable = set(string.printable)
    for sentence in sentences:
        if type(sentence) is str:
            s = ''.join(filter(lambda x: x in printable, sentence)).strip('\' .,-"=+><@!#$%^&*():')
            s_words = [w for w in nltk.wordpunct_tokenize(s) if w.lower() in words]
            if len(s_words) > 8:
                english_sentences.append(s)
    return english_sentences


def filter_english_tweets():
    df = pd.read_csv(constants.PREPROCESSED_TWEETS_PATH)
    english_tweets = filter_english(df['text'])
    s = '\n\n'.join(english_tweets)
    with open(constants.PROCESSED_TWEETS_PATH, 'w') as f:
        f.write(s)


def filter_english_fb():
    english_posts = []
    for f_path in constants.PREPROCESSED_FB_POSTS_PATH:
        df = pd.read_csv(f_path, error_bad_lines=False)
        bb_df = df[df['mk_name'] == 'בנימין נתניהו']
        bb_posts = bb_df['parent_status_content']
        english_posts.extend(filter_english(bb_posts))
    english_posts = list(set(english_posts))
    s = '\n\n'.join(english_posts)
    with open(constants.PROCESSED_FB_POSTS_PATH, 'w') as f:
        f.write(s)
