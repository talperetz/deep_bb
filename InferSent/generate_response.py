#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Date: 10/25/17
:TL;DR: deep_bb chat component
:Abstract: DataHack 2017 - 2 days hackaton
:Problem: given a small amount of sentences and a smaller amount of q&a build a functioning chatbot
:Proposed Solution: use sentence embedding and cosine similarity to relate query to question,
if there is no related question try relating a sentence,
if there is no related sentence use a trained chatbot,
if the chatbot isn't confident generate random general response
"""

import torch
import nltk
import pickle
from deep_bb.abstracts import Responder
from deep_bb import constants
from deep_bb.utils import get_stored_objects, store_objects
import numpy as np
from scipy import spatial
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import re


__author__ = "Tal Peretz"
__copyright__ = "Copyright 2017"
__maintainer__ = "Tal Peretz"
__email__ = "talp@panorays.com"
__status__ = "Development"


class QueryResponder(Responder):
    chatbot_responder = None
    general_responder = None

    def __init__(self):
        self.chatbot_responder = ChatbotResponder().preprocess()
        self.general_responder = GeneralResponder()

    def preprocess(self, qna_list, quotes):
        infersent = torch.load(constants.INFERSENT_ALL_NLI_PATH, map_location=lambda storage, loc: storage)
        infersent.set_glove_path(constants.INFERSENT_GLOVE_PATH)
        sentences = [d['question'].decode('utf-8').strip() for d in qna_list]
        sentences.extend(quotes)
        infersent.build_vocab(sentences, tokenize=True)
        embedded_sentences_matrix = infersent.encode(sentences, tokenize=True)

        # save to disk
        torch.save(infersent, constants.CHAT_INFERSENT_MODEL_PATH)
        store_objects({constants.CHAT_EMBEDDED_SENTENCES_MATRIX_PATH:embedded_sentences_matrix, constants.PROCESSED_QNA_PATH:qna_list, constants.CHAT_PROCESSED_SENTENCES_PATH:sentences})

    def preprocess_query(self, query):
        infersent = torch.load(constants.CHAT_INFERSENT_MODEL_PATH)
        sentence = query.lower().decode('utf-8').strip()
        return infersent.encode([sentence])[0]

    def reply(self, query):
        """
        TODO: improve according to
        https://stackoverflow.com/questions/17627219/whats-the-fastest-way-in-python-to-calculate-cosine-similarity-given-sparse-mat
        :param query: string representing question or sentence
        :return: string response
        """

        # load from disk
        embedded_sentences_matrix, qna_list, sentences = get_stored_objects(constants.CHAT_EMBEDDED_SENTENCES_MATRIX_PATH, constants.PROCESSED_QNA_PATH, constants.CHAT_PROCESSED_SENTENCES_PATH)

        query_vec = self.preprocess_query(query)

        cosine_similarities = []
        for v in embedded_sentences_matrix:
            cosine_similarities.append(1 - spatial.distance.cosine(query_vec, v))
        closest_sentence_idx, max_cosine_similarity = np.nanargmax(cosine_similarities), np.max(cosine_similarities)

        if max_cosine_similarity > constants.SIMILARITY_THRESHOLD:
            if closest_sentence_idx < len(qna_list):
                return qna_list[closest_sentence_idx]['answer']
            else:
                return sentences[closest_sentence_idx]
        else:
            reply, confidence = self.chatbot_responder.reply(query)
            if confidence > constants.CHATTER_CONFIDENCE_THRESHOLD:
                return reply
            else:
                return self.general_responder.reply(query)


class ChatbotResponder(Responder):
    chatbot = None

    def preprocess(self):
        self.chatbot = ChatBot(
            'deep_bb',
        )
        self.chatbot.set_trainer(ChatterBotCorpusTrainer)
        self.chatbot.train(
            "chatterbot.corpus.english.greetings",
            "chatterbot.corpus.english.conversations",
            "chatterbot.corpus.hebrew.conversations"
            # "chatterbot.corpus.english.history",
            # "chatterbot.corpus.english.politics"
        )
        return self

    def reply(self, query):
        response = self.chatbot.get_response(query)
        return response.text, response.confidence


class GeneralResponder(Responder):

    def reply(self, query):
        return np.random.choice(constants.GENERAL_RESPONSES, 1)[0]


if __name__ == '__main__':
    # usage example:

    qr = QueryResponder()
    with open(constants.PROCESSED_QNA_PATH) as f:
        qna_list = pickle.load(f)
    with open(constants.PROCESSED_QUOTES_PATH) as f:
        text = f.read().lower().decode('utf-8').strip()
    with open(constants.PROCESSED_FB_POSTS_PATH) as f:
        text = text + '\n\n' + f.read().lower().decode('utf-8').strip()
    for path in constants.PROCESSED_SPEECHES_PATHS:
        with open(path, 'r') as corpus:
            text += re.sub(pattern='\n+', repl='\n\n', string=corpus.read().lower()).decode('utf-8').strip() + '\n\n'

    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = tokenizer.tokenize(text)
    qr.preprocess(qna_list, sentences)
    query = 'how is it to be a prime minister?'
    print qr.reply(query) + '\n'
    query = 'do you like israel?'
    print qr.reply(query) + '\n'
    query = 'will there ever be peace?'
    print qr.reply(query) + '\n'
    query = 'how are you?'
    print qr.reply(query) + '\n'
    query = 'hi'
    print qr.reply(query) + '\n'
