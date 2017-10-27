import re

from controllers.Controller import Controller

from deep_bb import constants
from deep_bb.generate_speech import MccSpeechGenerator

DEEP_BB_PREFIX_PATH = 'deep_bb/deep_bb/'


class SpeechController(Controller):
    def __init__(self):
        Controller.__init__(self)

        texts = ''
        for path in constants.PROCESSED_SPEECHES_PATHS:
            with open(path, 'r') as corpus:
                texts += re.sub(pattern='\n+', repl='\n\n', string=corpus.read().lower()).strip() + '\n\n'
        self.mcc_speech_generator = MccSpeechGenerator().preprocess(texts)

    def _generate_speech(self):
        data = dict()
        data['speech'], data['statistics'] = self.mcc_speech_generator.generate_speech()
        data['statistics'] = dict(data['statistics'])
        data['sort_by_values'] = dict()
        data['sort_by_values_words'] = list()
        data['sort_by_values_counts'] = list()

        for w in sorted(data['statistics'], key=data['statistics'].get, reverse=True):
            data['sort_by_values_words'] = w
            data['sort_by_values_counts'] = data['statistics'][w]
        data['statistics_words'] = sorted(data.get('statistics').keys())
        data['statistics_counts'] = list()
        for word_count in data['statistics_words']:
            data['statistics_counts'].append(data['statistics'][word_count])
        return data
