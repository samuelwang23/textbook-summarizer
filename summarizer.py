# importing libraries
import nltk
nltk.download('punkt')
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
import bs4 as BeautifulSoup
import urllib.request
import pdb
from collections import defaultdict

from helpers import _get_file_contents, _get_ineligibles, _get_transition_words
from consts import __TRANSITION_WORDS__

class Sentence:
	def __init__(self, text, position):
		self.text = text
		self.tokens = word_tokenize(text)
		self.position = position

	def __len__(self):
		return len(self.text.split())

	def __lt__(self, sentence_b):
		return self.position < sentence_b.position


def _get_sentences(section):
	# Tokenize Sentences
	return [Sentence(text, pos) for pos, text in enumerate(sent_tokenize(section))]

class FrequencyScorer:
	def __init__(self, text):
		self.text = text
		self.sentences = _get_sentences(text)
		self._create_frequency_table()
		self._get_scores()

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

	def _get_scores(self):
		self.scores = []
		for sentence in self.sentences:
			self.scores.append((self._get_sentence_score(sentence), sentence))

class Summarizer:
	def __init__(self, scores, length):
		self.scores = scores
		self.length = length
		self.summarize()
		self.get_summary_text()

	def summarize(self):
		self.summary = []
		length = 0
		for pair in sorted(self.scores)[::-1]:
			if length < self.length:
				self.summary.append(pair[1])
				length += len(pair[1])
			else:
				return

	def get_summary_text(self):
		self.text = ""
		for sentence in sorted(self.summary):
			self.text += sentence.text + " "

scores = FrequencyScorer(_get_file_contents("test.txt")).scores

print(Summarizer(scores, 300).text)
