import os
import re

from controllers.Controller import Controller
from utils import tweeter_utils
import pickle
import nltk
from deep_bb import constants
from generate_response import QueryResponder
import traceback

DEEP_BB_PREFIX_PATH = '../deep_bb/'


class ChatController(Controller):
    def __init__(self):
        Controller.__init__(self)

        self._qr = QueryResponder()
        with open(constants.PROCESSED_QNA_PATH) as f:
            qna_list = pickle.load(f)
        with open(constants.PROCESSED_QUOTES_PATH) as f:
            text = f.read().lower().decode('utf-8').strip()
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        sentences = tokenizer.tokenize(text)
        if not os.path.exists(constants.INFERSENT_MODEL_PATH):
            self._engine = self._qr.preprocess(qna_list, sentences)

    def _answer(self, question):
        reply = 'fuck you!'
        try:
            reply = self._qr.reply(question)
            print reply
        except:
            traceback.format_exc()
        return reply
