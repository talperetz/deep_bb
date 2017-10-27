from controllers.Controller import Controller
from deep_bb import constants
from deep_bb.generate_speech import MccSpeechGenerator
import random

DEEP_BB_PREFIX_PATH = 'deep_bb/deep_bb/'


class SpeechController(Controller):
    def __init__(self):
        Controller.__init__(self)
        with open(constants.CORPUS_PATH, 'r') as corpus:
            text = corpus.read().lower()
        self.mcc_speech_generator = MccSpeechGenerator().preprocess(text)

    def _generate_speech(self):
        data = dict()
        data['speech'] = self.mcc_speech_generator.generate_speech()
        data['statistics'] = self._generate_speech_statistics()
        return data

    def _generate_speech_statistics(self):
        statistics = dict()
        statistics_words_qtt = random.randint(15, 40)
        for word_index in xrange(statistics_words_qtt):
            statistics[str(word_index)] = random.uniform(0, 50)
        return statistics
