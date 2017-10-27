from controllers.Controller import Controller
from deep_bb import constants
from deep_bb.generate_speech import MccSpeechGenerator
import random
import traceback
DEEP_BB_PREFIX_PATH = 'deep_bb/deep_bb/'


class SpeechController(Controller):
    def __init__(self):
        Controller.__init__(self)
        with open(constants.CORPUS_PATH, 'r') as corpus:
            text = corpus.read().lower()
        self.mcc_speech_generator = MccSpeechGenerator().preprocess(text)

    def _generate_speech(self):
        data = None
        try:
            data['speech'], data['statistics'] = self.mcc_speech_generator.generate_speech()
            data['statistics'] = dict(data['statistics'])
        except:
            traceback.format_exc()
        return data
