#!/usr/bin/env python

"""
:Date: 10/25/17
:TL;DR:
:Abstract:
:Problem:
:Proposed Solution:
"""
from abc import ABCMeta, abstractmethod
import markovify
import spacy
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
from scipy.interpolate import interp1d
import matplotlib
from matplotlib import pyplot as plt
plt.ioff()
matplotlib.use('Agg')


__author__ = "Tal Peretz"
__copyright__ = "Copyright 2017"
__maintainer__ = "Tal Peretz"
__email__ = "talp@panorays.com"
__status__ = "Development"


class SpeechGenerator:
    __metaclass__ = ABCMeta
    model = None

    @abstractmethod
    def preprocess(self, text):
        pass

    @abstractmethod
    def generate_speech(self, n_sentences=50):
        pass


class POSifiedText(markovify.Text):
    nlp = spacy.load("en")

    def word_split(self, sentence):
        # sentence = sentence.decode('utf-8')
        return ["::".join((word.orth_, word.pos_)) for word in self.nlp(sentence)]

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


class MccSpeechGenerator(SpeechGenerator):

    def preprocess(self, text):
        mc_model = markovify.Text(text, state_size=3)
        # mc_model = POSifiedText(text, state_size=2)
        with open(constants.SPEECH_MODEL_PATH, 'wb') as f:
            pickle.dump(mc_model, f)
        return self

    def generate_intro(self):
        return ['ladies and gentlemen,']

    def generate_sentence(self, mc_model, sentences):
            s = None
            while not s or s in sentences:
                s = mc_model.make_sentence()
            return s

    def generate_speech(self, sentence_starter=None, n_sentences=15):
        with open(constants.SPEECH_MODEL_PATH, 'rb') as f:
            mc_model = pickle.load(f)
        output = list()
        intro = self.generate_intro()
        output.extend(intro)
        for i in range(n_sentences - len(intro)):
            output.append(self.generate_sentence(mc_model, output))
        blank_with_punct = r"\s+[',.!?]+"

        def rep(m):
            return m.group(0).replace(r' ', '')

        corrected_output = [re.sub(blank_with_punct, rep, sentence) for sentence in output]
        return '\n'.join(corrected_output)


class MccEmbeddedSpeechGenerator(SpeechGenerator):

    def preprocess(self, texts):
        mc_models = []
        for text in texts:
            mc_models.append(markovify.Text(text.lower(), state_size=3))
        combined_model = markovify.combine(mc_models)
        # mc_model = POSifiedText(text, state_size=3)
        with open(constants.SPEECH_MODEL_PATH, 'wb') as f:
            pickle.dump(combined_model, f)
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        sentences = [sentence.decode('utf-8').strip() for sentence in tokenizer.tokenize(text)]
        infersent = torch.load(constants.INFERSENT_ALL_NLI_PATH, map_location=lambda storage, loc: storage)
        infersent.set_glove_path(constants.INFERSENT_GLOVE_PATH)
        infersent.build_vocab(sentences, tokenize=True)
        torch.save(infersent, constants.CHAT_INFERSENT_MODEL_PATH)
        embedded_sentences_matrix = infersent.encode(sentences, tokenize=True)
        with open(constants.SPEECH_EMBEDDED_SENTENCES_MATRIX_PATH, 'wb') as f:
            pickle.dump(embedded_sentences_matrix, f)
        with open(constants.SPEECH_PROCESSED_SENTENCES_PATH, 'wb') as f:
            pickle.dump(sentences, f)
        return self

    def generate_intro(self):
        return ['ladies and gentlemen,']

    def generate_sentence(self, mc_model):
            s = None
            while not s:
                s = mc_model.make_sentence()
            return s

    def generate_speech(self, sentence_starter=None, n_sentences=15):
        with open(constants.SPEECH_MODEL_PATH, 'rb') as f:
            mc_model = pickle.load(f)

        with open(constants.SPEECH_EMBEDDED_SENTENCES_MATRIX_PATH, 'rb') as f:
            embedded_sentences_matrix = pickle.load(f)
        with open(constants.PROCESSED_QNA_PATH, 'rb') as f:
            qna_list = pickle.load(f)
        with open(constants.SPEECH_PROCESSED_SENTENCES_PATH, 'rb') as f:
            sentences = pickle.load(f)

        # query_vec = self.preprocess_query(query)
        # cosine_similarities = []
        # for v in embedded_sentences_matrix:
        #     cosine_similarities.append(1 - spatial.distance.cosine(query_vec, v))
        # closest_sentence_idx, max_cosine_similarity = np.nanargmax(cosine_similarities), np.max(cosine_similarities)
        # if max_cosine_similarity > constants.SIMILARITY_THRESHOLD:
        #     if closest_sentence_idx < len(qna_list):
        #         return qna_list[closest_sentence_idx]['answer']

        output = list()
        intro = self.generate_intro()
        output.extend(intro)
        for i in range(n_sentences - len(intro)):
            output.append(self.generate_sentence(mc_model))
        blank_with_punct = r"\s+[',.!?]+"

        def rep(m):
            return m.group(0).replace(r' ', '')

        corrected_output = [re.sub(blank_with_punct, rep, sentence) for sentence in output]
        return '\n'.join(corrected_output)


class MccTopicBasedSpeechGenerator(SpeechGenerator):

    def preprocess(self, texts):
        try:
            with open(constants.LDA_CLUSTERS_PATH, 'rb') as f:
                topic_to_docs = pickle.load(f)
        except:
            topic_to_docs = TopicModeling().get_clusters(texts)
        mc_models = []
        # topics = np.random.choice(constants.LDA_N_TOPICS, constants.LDA_N_TOPICS_FOR_SPEECH)
        topics = np.arange(0, constants.LDA_N_TOPICS)
        for topic in topics:
            mc_models.append(POSifiedText(topic_to_docs[topic], state_size=2))
            # mc_models.append(markovify.Text(topic_to_docs[topic], state_size=2))
        with open(constants.SPEECH_MODELS_PATH, 'wb') as f:
            pickle.dump(mc_models, f)
        return self

    def generate_sentence(self, mc_model, sentences):
            s = None
            while s is None or s in sentences:
                s = mc_model.make_sentence()
            return s

    def generate_speech(self, sentence_starter=None, n_sentences=23):
        with open(constants.SPEECH_MODELS_PATH, 'rb') as f:
            mc_models = pickle.load(f)
        output = list()
        m = interp1d([0, n_sentences - len(intro)], [0, len(mc_models)])
        for i in range(n_sentences - len(intro)):
            mc_model = mc_models[int(m(i))]
            output.append(self.generate_sentence(mc_model, output))
        blank_with_punct = r"\s+[',.!?]+"

        def rep(m):
            return m.group(0).replace(r' ', '')

        corrected_output = [re.sub(blank_with_punct, rep, sentence) for sentence in output]
        return '\n'.join(corrected_output)


class TopicModeling:

    def get_importatnt_words(self, sentence):
        """
        this function filters only important words from a sentence
        """
        infersent = torch.load(constants.SPEECH_INFERSENT_MODEL_PATH)
        out, idxs = infersent.visualize(sentence, tokenize=True)
        argmaxs = [np.sum((idxs == k)) for k in range(len(sentence.split()) + 2)]
        args_importance = [100.0 * n / np.sum(argmaxs) for n in argmaxs][1:-1]
        average_importance = np.mean(args_importance)
        important_words = [sentence.split()[i] for i in range(0, len(args_importance)) if
                           args_importance[i] > average_importance]
        return important_words

    def preprocess_paragraphs(self, paragraphs):
        tokenizer = RegexpTokenizer(r'\w+')

        en_stop = get_stop_words('en')
        p_stemmer = PorterStemmer()
        docs = []
        for paragraph in paragraphs:
            raw = paragraph.lower()
            tokens = tokenizer.tokenize(raw)
            stopped_tokens = [i for i in tokens if i not in en_stop]
            # important_tokens = self.get_importatnt_words(' '.join(stopped_tokens))
            stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
            docs.append(stemmed_tokens)
        return docs

    def get_bow(self, docs):
        dictionary = corpora.Dictionary(docs)
        bow = [dictionary.doc2bow(doc) for doc in docs]
        return bow, dictionary

    def get_clusters(self, texts):
        paragraphs = []
        for text in texts:
            # paragraphs.extend([sentence.decode('utf-8').strip() for sentence in re.split(pattern=r'\n\n\n+',string=text)])
            paragraphs.extend([sentence.decode('utf-8').strip() for sentence in re.split(r'\n+', text)])
        infersent = torch.load(constants.INFERSENT_ALL_NLI_PATH, map_location=lambda storage, loc: storage)
        infersent.set_glove_path(constants.INFERSENT_GLOVE_PATH)
        infersent.build_vocab(paragraphs, tokenize=True)
        torch.save(infersent, constants.SPEECH_INFERSENT_MODEL_PATH)
        bow, dictionary = self.get_bow(self.preprocess_paragraphs(paragraphs))
        lda = gensim.models.ldamodel.LdaModel(bow, num_topics=constants.LDA_N_TOPICS, id2word=dictionary, passes=constants.LDA_N_PASSES)

        # Assigns the topics to the documents in corpus
        lda_corpus = lda[bow]

        scores = list(chain(*[[score for topic_id, score in topic] for topic in [doc for doc in lda_corpus]]))
        threshold = sum(scores) / len(scores)
        print threshold
        topic_to_docs = {}
        for topic_idx in range(lda.num_topics):
            topic_to_docs[topic_idx] = [sentence for lda_scores, sentence in zip(lda_corpus, paragraphs) if
                            len(lda_scores) == lda.num_topics and lda_scores[topic_idx][1] > threshold]
        with open(constants.LDA_CLUSTERS_PATH, 'wb') as f:
            pickle.dump(topic_to_docs, f)
        print lda.print_topics(num_topics=constants.LDA_N_TOPICS, num_words=4)
        print '\n'
        return topic_to_docs


if __name__ == '__main__':

    with open(constants.CORPUS_PATH, 'r') as corpus:
        text = corpus.read().lower()


    texts = ''
    for path in constants.PROCESSED_SPEECHES_PATHS:
        with open(path, 'r') as corpus:
            texts += re.sub(pattern='\n+', repl='\n\n', string=corpus.read().lower()).strip() + '\n\n'

    # mcc_speech_generator = MccTopicBasedSpeechGenerator().preprocess(texts)
    # print(mcc_speech_generator.generate_speech(constants.PROCESSED_SPEECHES_PATHS))

    mcc_speech_generator = MccSpeechGenerator().preprocess(texts)
    print(mcc_speech_generator.generate_speech())
