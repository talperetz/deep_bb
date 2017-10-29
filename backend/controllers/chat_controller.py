import os
import re

from controllers.Controller import Controller
from utils import tweeter_utils
import pickle
import nltk
from deep_bb import constants
from generate_response import QueryResponder
import traceback
import random

DEEP_BB_PREFIX_PATH = '../deep_bb/'

possible_answers = ['im on a meeting with Trump, try again later',
                    'Sara just called me, i have to go to take out the puppies']


class ChatController(Controller):
    def __init__(self):
        Controller.__init__(self)

        self._qr = QueryResponder()
        with open(constants.PROCESSED_QNA_PATH) as f:
            qna_list = pickle.load(f)
        with open(constants.PROCESSED_QUOTES_PATH) as f:
            text = f.read().lower().decode('utf-8').strip()
        with open(constants.PROCESSED_FB_POSTS_PATH) as f:
            text = text + '\n\n' + f.read().lower().decode('utf-8').strip()
        for path in constants.PROCESSED_SPEECHES_PATHS:
            with open(path, 'r') as corpus:
                text += re.sub(pattern='\n+', repl='\n\n', string=corpus.read().lower()).decode(
                    'utf-8').strip() + '\n\n'
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        sentences = tokenizer.tokenize(text)
        if not os.path.exists(constants.CHAT_INFERSENT_MODEL_PATH):
            self._engine = self._qr.preprocess(qna_list, sentences)

    def _answer(self, question):
        reply = possible_answers[random.randint(0, len(possible_answers) - 1)]
        try:
            reply = self._qr.reply(question)
            print reply
        except:
            traceback.format_exc()
        return reply
