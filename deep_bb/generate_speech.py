#!/usr/bin/env python

"""
:Date: 10/25/17
:TL;DR: deep_bb speech component
:Abstract: DataHack 2017 - 2 days hackaton
:Problem: given a minuscule amount of speeches create a bb speech generator
:Proposed Solutions:
1. markov chains sentence generator where 2 sentences cannot be identical in speech
2. markov chains sentence generator per topic, after performing topic modeling with LDA, in a certain clusters order
3. markov chains sentence generator, where next sentence must be in a certain distance from the next,
assuming too close distance will result in identical content, and too far will result in a context break.
"""
import markovify
import constants
import re
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
import nltk
from nltk.stem.porter import PorterStemmer
from gensim import corpora
import gensim
import torch
import pickle
import numpy as np
from itertools import chain
from scipy import spatial
from deep_bb.abstracts import SpeechGenerator
from deep_bb.utils import POSifiedText, get_word_occurences, generate_sentence, generate_intro, correct_puctuation, split_approx, filter_bad_sentences, get_stored_objects, store_objects


__author__ = "Tal Peretz"
__copyright__ = "Copyright 2017"
__maintainer__ = "Tal Peretz"
__email__ = "talp@panorays.com"
__status__ = "Development"


class MccSpeechGenerator(SpeechGenerator):

    def preprocess(self, text):
        mc_model = markovify.Text(text, state_size=3)
        # mc_model = POSifiedText(text, state_size=2)
        store_objects({constants.SPEECH_MODEL_PATH:mc_model})
        return self

    def generate_speech(self, n_sentences=15, n_words=15):
        mc_model = get_stored_objects(constants.SPEECH_MODEL_PATH)
        intro = generate_intro()
        output = [intro]
        for i in range(n_sentences - len(output)):
            output.append(generate_sentence(mc_model, output))
        speech = '\n'.join(correct_puctuation(output))
        return speech, get_word_occurences(speech, n_words)


class MccEmbeddedSpeechGenerator(SpeechGenerator):

    def preprocess(self, texts):
        mc_model = markovify.Text(texts.lower(), state_size=3)
        texts = '\n\n'.join(filter_bad_sentences(re.split('\n+', texts)))
        # mc_model = POSifiedText(unicode(texts), state_size=3)
        with open(constants.SPEECH_MODEL_PATH, 'wb') as f:
            pickle.dump(mc_model, f)
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        sentences = [sentence for sentence in tokenizer.tokenize(texts)]
        infersent = torch.load(constants.INFERSENT_ALL_NLI_PATH, map_location=lambda storage, loc: storage)
        infersent.set_glove_path(constants.INFERSENT_GLOVE_PATH)
        infersent.build_vocab(sentences, tokenize=True)
        torch.save(infersent, constants.SPEECH_INFERSENT_MODEL_PATH)
        return self

    def preprocess_sentence(self, sentence):
        infersent = torch.load(constants.SPEECH_INFERSENT_MODEL_PATH)
        sentence = sentence.lower().decode('utf-8').strip()
        return infersent.encode([sentence])[0]

    def generate_speech(self, n_sentences=15, n_words=15):
        with open(constants.SPEECH_MODEL_PATH, 'rb') as f:
            mc_model = pickle.load(f)

        output = [generate_intro()]
        output.append(generate_sentence(mc_model, output))
        sent_vec = self.preprocess_sentence(output[-1])
        sentences_vectors = []
        while len(output) < n_sentences:
            candidate_sentence = generate_sentence(mc_model, output)
            v = self.preprocess_sentence(candidate_sentence)
            last_sentence_cosine_similarity = (1 - spatial.distance.cosine(sent_vec, v))
            if 0.7 < last_sentence_cosine_similarity < 0.9:
                is_duplicated = False
                for vec in sentences_vectors:
                    past_sentences_cosine_similarity = (1 - spatial.distance.cosine(vec, v))
                    if past_sentences_cosine_similarity > 0.94:
                        is_duplicated = True
                if not is_duplicated:
                    output.append(candidate_sentence)
                    sentences_vectors.append(v)
        speech = '\n'.join(correct_puctuation(output))
        return speech, get_word_occurences(speech, n_words)


class MccTopicBasedSpeechGenerator(SpeechGenerator):

    def preprocess(self, texts):
        try:
            topic_to_docs = get_stored_objects(constants.LDA_CLUSTERS_PATH)
        except:
            topic_to_docs = TopicModeling().get_clusters(texts)
        mc_models = []
        # topics = np.random.choice(constants.LDA_N_TOPICS, constants.LDA_N_TOPICS_FOR_SPEECH)
        topics = np.arange(0, constants.LDA_N_TOPICS)
        for topic in topics:
            # mc_models.append(POSifiedText(topic_to_docs[topic], state_size=2))
            mc_models.append(markovify.Text(topic_to_docs[topic], state_size=2))
        with open(constants.SPEECH_MODELS_PATH, 'wb') as f:
            pickle.dump(mc_models, f)
        return self

    def get_topic_structure(self, n_sentences):
        topic_structure = list()
        speech_structure = split_approx(n_sentences, constants.SPEECH_N_TOPICS)
        for k in speech_structure:
            topic_structure.extend(np.random.choice(constants.LDA_TOPICS_MAP['main'], k))
            topic_structure.append(constants.LDA_TOPICS_MAP['continue'])
        topic_structure.append(constants.LDA_TOPICS_MAP['end'])
        return topic_structure

    def generate_speech(self, n_sentences=15, n_words=15):
        with open(constants.SPEECH_MODELS_PATH, 'rb') as f:
            mc_models = pickle.load(f)
        output = [generate_intro()]

        topic_structure = self.get_topic_structure(n_sentences)

        for i in topic_structure:
            output.append(generate_sentence(mc_models[i], output))
        speech = '\n'.join(correct_puctuation(output))
        return speech, get_word_occurences(speech, n_words)


class TopicModeling:

    def preprocess_paragraphs(self, paragraphs):
        tokenizer = RegexpTokenizer(r'\w+')

        en_stop = get_stop_words('en')
        p_stemmer = PorterStemmer()
        docs = []
        for paragraph in paragraphs:
            raw = paragraph.lower()
            tokens = tokenizer.tokenize(raw)
            stopped_tokens = [i for i in tokens if i not in en_stop]
            # important_tokens = get_importatnt_words(' '.join(stopped_tokens))
            stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
            docs.append(stemmed_tokens)
        return docs

    def get_bow(self, docs):
        dictionary = corpora.Dictionary(docs)
        bow = [dictionary.doc2bow(doc) for doc in docs]
        return bow, dictionary

    def get_clusters(self, texts):
        sentences = list()
        for text in texts:
            sentences.extend([sentence.decode('utf-8').strip() for sentence in re.split(r'\n+', text)])
        infersent = torch.load(constants.INFERSENT_ALL_NLI_PATH, map_location=lambda storage, loc: storage)
        infersent.set_glove_path(constants.INFERSENT_GLOVE_PATH)
        infersent.build_vocab(sentences, tokenize=True)
        torch.save(infersent, constants.SPEECH_INFERSENT_MODEL_PATH)
        bow, dictionary = self.get_bow(self.preprocess_paragraphs(sentences))
        lda = gensim.models.ldamodel.LdaModel(bow, num_topics=constants.LDA_N_TOPICS, id2word=dictionary, passes=constants.LDA_N_PASSES)

        # Assigns the topics to the documents in corpus
        lda_corpus = lda[bow]

        scores = list(chain(*[[score for topic_id, score in topic] for topic in [doc for doc in lda_corpus]]))
        threshold = sum(scores) / len(scores)
        print threshold
        topic_to_docs = {}
        for topic_idx in range(lda.num_topics):
            topic_to_docs[topic_idx] = [sentence for lda_scores, sentence in zip(lda_corpus, sentences) if
                            len(lda_scores) == lda.num_topics and lda_scores[topic_idx][1] > threshold]
        store_objects({constants.LDA_CLUSTERS_PATH:topic_to_docs})
        print lda.print_topics(num_topics=constants.LDA_N_TOPICS, num_words=4)
        print '\n'
        return topic_to_docs


if __name__ == '__main__':
    # usage examples

    texts = ''
    for path in constants.PROCESSED_SPEECHES_PATHS:
        with open(path, 'r') as corpus:
            texts += re.sub(pattern='\n+', repl='\n\n', string=corpus.read().lower()).strip() + '\n\n'

    mcc_speech_generator = MccSpeechGenerator().preprocess(texts)
    speech, wc = mcc_speech_generator.generate_speech()
    print speech + '\n\n'

    mcc_speech_generator = MccTopicBasedSpeechGenerator().preprocess(texts)
    speech, wc = mcc_speech_generator.generate_speech()
    print speech +'\n\n'

    mcc_speech_generator = MccEmbeddedSpeechGenerator().preprocess(texts)
    speech, wc = mcc_speech_generator.generate_speech()
    print speech + '\n\n'
