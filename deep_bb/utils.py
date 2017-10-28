#!/usr/bin/env python

"""
:Date: 10/28/17
:TL;DR: common utility functions
"""

import torch
import pickle
import markovify
import spacy
from deep_bb import constants
from stop_words import get_stop_words
from string import punctuation
from collections import Counter
import re


def store_objects(path_to_object):
    for p, obj in path_to_object.items():
        with open(p, 'wb') as f:
            pickle.dump(obj, f)


def get_stored_objects(*paths):
    objects = list()
    for p in paths:
        with open(p, 'rb') as f:
            objects.append(pickle.load(f))
    return objects[0] if len(objects) == 1 else tuple(objects)


class POSifiedText(markovify.Text):
    nlp = spacy.load("en")

    def word_split(self, sentence):
        # sentence = sentence.decode('utf-8')
        return ["::".join((word.orth_, word.pos_)) for word in self.nlp(sentence)]

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


def get_importatnt_words(sentence):
    """
    this function filters only important words from a sentence using facebook's infersent
    """
    infersent = torch.load(constants.SPEECH_INFERSENT_MODEL_PATH)
    out, idxs = infersent.visualize(sentence, tokenize=True)
    argmaxs = [np.sum((idxs == k)) for k in range(len(sentence.split()) + 2)]
    args_importance = [100.0 * n / np.sum(argmaxs) for n in argmaxs][1:-1]
    average_importance = np.mean(args_importance)
    important_words = [sentence.split()[i] for i in range(0, len(args_importance)) if
                       args_importance[i] > average_importance]
    return important_words


def get_word_occurences(text, n):
    stop_words = get_stop_words('en')
    linewords = text.translate(None, punctuation).lower().split()
    freq = dict(Counter(linewords))
    for k, v in freq.items():
        if k in stop_words:
            del freq[k]
    return Counter(freq).most_common(n)


def generate_sentence(mc_model, sentences):
        s = None
        while not s or s in sentences:
            s = mc_model.make_sentence()
        try:
            s = str(s)
        except UnicodeEncodeError:
            s = generate_sentence(mc_model, sentences + [s])
        return s


def filter_bad_sentences(sentences):
    filtered_sentences = []
    for s in sentences:
        try:
            filtered_sentences.append(s.decode('utf-8'))
        except UnicodeEncodeError:
            pass
    return filtered_sentences


def generate_intro():
    return 'ladies and gentlemen,'


def correct_puctuation(sentences):
    blank_with_punct = r"\s+[',.!?]+"

    def rep(m):
        return m.group(0).replace(r' ', '')

    corrected_output = [re.sub(blank_with_punct, rep, sentence) for sentence in sentences]
    return corrected_output


def split_approx(num, div):
    remainder = num % div
    integer = num / div
    splits = []
    for i in range(div):
        splits.append(integer)
    for i in range(remainder):
        splits[i] += 1
    return splits
