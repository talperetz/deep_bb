import os
import re

from controllers.Controller import Controller
from utils import tweeter_utils
import pickle
import nltk
from deep_bb import constants
from InferSent.generate_response import QueryResponder

DEEP_BB_PREFIX_PATH = '../deep_bb/'


class ChatController(Controller):
    def __init__(self):
        Controller.__init__(self)

        qr = QueryResponder()
        with open(constants.PROCESSED_QNA_PATH) as f:
            qna_list = pickle.load(f)
        with open(constants.PROCESSED_QUOTES_PATH) as f:
            text = f.read().lower().decode('utf-8').strip()
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        sentences = tokenizer.tokenize(text)
        self._engine = qr.preprocess(qna_list, sentences)

    def _answer(self, question):
        try:
            return self._engine.reply(question)
        except:
            pass
        return 'fuck you!'
