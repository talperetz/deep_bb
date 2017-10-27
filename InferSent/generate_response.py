#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Date: 10/25/17
:TL;DR:
:Abstract:
:Problem:
:Proposed Solution:
"""

import torch
import nltk
import pickle
from abc import ABCMeta, abstractmethod
from deep_bb import constants
import numpy as np
from scipy import spatial
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
import re


__author__ = "Tal Peretz"
__copyright__ = "Copyright 2017"
__maintainer__ = "Tal Peretz"
__email__ = "talp@panorays.com"
__status__ = "Development"


class Responder:
    __metaclass__ = ABCMeta

    @abstractmethod
    def preprocess_query(self, query):
        pass

    @abstractmethod
    def reply(self, query):
        pass


class QueryResponder(Responder):
    general_responder = None

    def __init__(self):
        self.general_responder = GeneralResponder().preprocess()

    def preprocess(self, qna_list, quotes):
        infersent = torch.load(constants.INFERSENT_ALL_NLI_PATH, map_location=lambda storage, loc: storage)
        infersent.set_glove_path(constants.INFERSENT_GLOVE_PATH)
        sentences = [d['question'].decode('utf-8').strip() for d in qna_list]
        sentences.extend(quotes)
        infersent.build_vocab(sentences, tokenize=True)
        torch.save(infersent, constants.CHAT_INFERSENT_MODEL_PATH)
        embedded_sentences_matrix = infersent.encode(sentences, tokenize=True)
        with open(constants.CHAT_EMBEDDED_SENTENCES_MATRIX_PATH, 'wb') as f:
            pickle.dump(embedded_sentences_matrix, f)
        with open(constants.PROCESSED_QNA_PATH, 'wb') as f:
            pickle.dump(qna_list, f)
        with open(constants.CHAT_PROCESSED_SENTENCES_PATH, 'wb') as f:
            pickle.dump(sentences, f)

    def preprocess_query(self, query):
        infersent = torch.load(constants.CHAT_INFERSENT_MODEL_PATH)
        sentence = query.lower().decode('utf-8').strip()
        return infersent.encode([sentence])[0]

    def reply(self, query):
        # improve according to
        # https://stackoverflow.com/questions/17627219/whats-the-fastest-way-in-python-to-calculate-cosine-similarity-given-sparse-mat
        # since the matrix is very sparse !!!!!!!!!!!!!!!!!!
        with open(constants.CHAT_EMBEDDED_SENTENCES_MATRIX_PATH, 'rb') as f:
            embedded_sentences_matrix = pickle.load(f)
        with open(constants.PROCESSED_QNA_PATH, 'rb') as f:
            qna_list = pickle.load(f)
        with open(constants.CHAT_PROCESSED_SENTENCES_PATH, 'rb') as f:
            sentences = pickle.load(f)
        query_vec = self.preprocess_query(query)
        cosine_similarities = []
        for v in embedded_sentences_matrix:
            cosine_similarities.append(1 - spatial.distance.cosine(query_vec, v))
        closest_sentence_idx, max_cosine_similarity = np.nanargmax(cosine_similarities), np.max(cosine_similarities)
        # if max_cosine_similarity > constants.SIMILARITY_THRESHOLD:
        if True:
            if closest_sentence_idx < len(qna_list):
                return qna_list[closest_sentence_idx]['answer']
            else:
                return sentences[closest_sentence_idx]
        else:
            reply, confidence = self.general_responder.reply(query)
            if confidence > constants.CHATTER_CONFIDENCE_THRESHOLD:
                return reply
            else:
                return np.random.choice(constants.GENERAL_RESPONSES, 1)[0]



# class QueryResponder(Responder):
#     topic_to_model = {}
#
#     def __init__(self):
#         with open('../models/trained_lda_model.pickle', 'rb') as f:
#             self.lda_model = pickle.load(f)
#         with open('../models/bow_dictionary.pickle', 'rb') as f:
#             self.bow_dictionary = pickle.load(f)
#
#     def preprocess_query(self, query):
#
#         # clean and tokenize document string
#         raw = query.lower()
#         tokenizer = RegexpTokenizer(r'\w+')
#         tokens = tokenizer.tokenize(raw)
#         # important_tokens = get_importatnt_words(' '.join(tokens))
#
#         # create English stop words list
#         en_stop = get_stop_words('en')
#         stopped_tokens = [i for i in tokens if not i in en_stop]
#
#         # Create p_stemmer of class PorterStemmer
#         p_stemmer = PorterStemmer()
#         stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
#         query_bow = [self.bow_dictionary.doc2bow(stemmed_tokens)]
#         return query_bow
#
#     def get_chosen_topic_relevance(self, query):
#         query_bow = self.preprocess_query(query)
#         doc_lda = self.lda_model[query_bow]
#         topic_relevance = max(list(doc_lda)[0], key=lambda tup: tup[1])[1]
#         return topic_relevance
#
#     def reply(self, query):
#         query_bow = self.preprocess_query(query)
#         doc_lda = self.lda_model[query_bow]
#         topic = max(list(doc_lda)[0], key=lambda tup: tup[1])[0]
#         self.topic_to_model[topic].generate_sentence()


class GeneralResponder(Responder):
    # https://github.com/gunthercox/ChatterBot
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

    def preprocess_query(self, query):
        return query

    def reply(self, query):
        response = self.chatbot.get_response(query)
        return response.text, response.confidence


if __name__ == '__main__':
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

