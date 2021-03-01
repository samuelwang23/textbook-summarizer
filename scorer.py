from helpers import _get_sentences, _get_ineligibles
from nltk.stem import PorterStemmer
from collections import defaultdict
from nltk.tokenize import word_tokenize
from consts import __TRANSITION_WORDS__

class FrequencyScorer:
    def __init__(self, text):
        self.text = text
        self.sentences = _get_sentences(text)
        self._create_frequency_table()
    
    def _create_frequency_table(self):
        # Get ineligibles and transition words
        ineligibles = _get_ineligibles()

        # Get a stemmer
        stemmer = PorterStemmer()
        frequency_table = defaultdict(int)
        
        for word in word_tokenize(self.text):
            # Reduce word to root form 
            word = stemmer.stem(word)
            word_weight = 1

            # remove Stop Words and Non alpha numerics
            if word in ineligibles:
                continue

            # Add weight if a transition word
            if word in __TRANSITION_WORDS__:
                word_weight += 100

            frequency_table[word] += word_weight

        self.frequency_table = frequency_table
    
    def _get_sentence_score(self, sentence):
        score = 0
        for token in sentence.tokens:
            score += self.frequency_table[token]
        return score / len(sentence)

    def _get_scores(self, sentences):
        scores = []
        for sentence in sentences:
            scores.append((self._get_sentence_score(sentence), sentence))
        return scores