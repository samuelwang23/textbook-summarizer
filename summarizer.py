#importing libraries
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
import bs4 as BeautifulSoup
import urllib.request
import pdb
from collections import defaultdict

__FILE_NAME__ = "text.txt"
lines_to_ignore = ["image pop up. Press enter to access the pop up"]

def _get_transition_words():
	return ["however", "yet", "although", "still", "despite"]

def _get_symbols():
	return set([".", ",", "|"])

def _get_file_contents(file_name):
	file_contents = ""
	file = open(file_name, "r")
	while(True):
		line = file.readline()
		if not line:
			break
		elif line in lines_to_ignore:
			continue
		else:
			file_contents += line
	return file_contents
def _get_ineligibles():
	stop_words = set(stopwords.words("english"))
	symbols = _get_symbols()
	return stop_words | symbols


def _eligible(word, ineligibles):
	return word in ineligibles

def _create_frequency_table(file_contents):
	# Get ineligibles and transition wrods
	ineligibles = _get_ineligibles()
	transition_words = _get_transition_words()


	# Tokenize words
	words = word_tokenize(file_contents)

	# Get a stemmer
	stemmer = PorterStemmer()

	frequency_table = defaultdict(int)
	for word in words:
		# Reduce word to root form
		word = stemmer.stem(word)

		word_weight = 1

		# remove Stop Words and Non alpha numerics
		if not _eligible(word, ineligibles):
			continue

		# Add weight if a transition word
		if word in transition_words:
			word_weight += 100

		frequency_table[word] += word_weight
	return frequency_table

def _split_into_sections(file_contents):
	return file_contents.split("##")

def _get_header(section):
	return section.split("\n")[0]

def _calculate_sentence_score(sentence, frequency_table):
	# Tokenize Sentence
	words = word_tokenize(sentence)

	sentence_score = 0
	sentence_word_count = 0
	for word in words:
		if word not in frequency_table:
			continue
		else:
			sentence_score += frequency_table[word]
			sentence_word_count += 1
	if sentence_word_count == 0:
		return 0
	else:
		return sentence_score/sentence_word_count

def _calculate_sentence_scores(sentences, frequency_table):
	sentence_scores = dict()
	for sentence in sentences:
		sentence_scores[hash(sentence)] = _calculate_sentence_score(sentence, frequency_table)
	return sentence_scores

def _get_hash_to_sentence(sentences):
	hash_to_sentence = dict()
	for sentence in sentences:
		hash_to_sentence[hash(sentence)] = sentence
	return hash_to_sentence

def _get_sentence_word_count(sentence):
	return len(sentence.split())

def _get_section_word_count(sentences):
	word_count = 0
	for sentence in sentences:
		word_count += _get_sentence_word_count(sentence)
	return word_count


def _get_top_sentences(sentence_scores, hash_to_sentence, section_word_count, mode):
	summary_word_count = 0
	top_sentences = []
	for hash in sentence_scores:
		sentence = hash_to_sentence[hash]
		summary_word_count += _get_sentence_word_count(sentence)

		reduction = 1 - summary_word_count / section_word_count
		top_sentences.append(hash)
		if reduction < mode:
			return top_sentences
	return top_sentences

def _get_sentence_locations(sentences):
	locations = dict()
	for index, sentence in enumerate(sentences, start=1):
		locations[hash(sentence)] = index
	return locations

def _order_sentences(top_sentences, locations, hash_to_sentence):
	sentences = []
	for hash in top_sentences:
		sentences.append((locations[hash], hash_to_sentence[hash]))
	return [v for k, v in sorted(sentences, key=lambda item: item[1])]

def _create_summary(sentences):
	summary = ""
	for sentence in sentences:
		summary += sentence + " "
	return summary

def _get_section_summary(section, mode, frequency_table):
	# Get the heading
	heading = _get_header(section)
	section_summary = "\n\n##" + heading + "\n"

	# Tokenize Sentences
	sentences = sent_tokenize(section)

	# Get Sentence Scores
	sentence_scores = _calculate_sentence_scores(sentences, frequency_table)

	# Sort Sentence Scores
	sentence_scores = {k: v for k, v in sorted(sentence_scores.items(), key=lambda item: item[1])}

	# Get hash to sentence and sentence locations
	hash_to_sentence = _get_hash_to_sentence(sentences)
	locations = _get_sentence_locations(sentences)

	# Get Section Word Count
	section_word_count = _get_section_word_count(sentences)

	#Get Top Sentences
	top_sentences = _get_top_sentences(sentence_scores, hash_to_sentence, section_word_count, mode)
	ordered_sentences = _order_sentences(top_sentences, locations, hash_to_sentence)

	#Create summary
	section_summary += _create_summary(ordered_sentences)
	return section_summary

def _get_file_summary(file_name, mode):
	# Get file contents
	file_contents = _get_file_contents(file_name)

	# Create the frequency table
	frequency_table = _create_frequency_table(file_contents)

	# Split article into sections
	sections = _split_into_sections(file_contents)

	article_summary = ""

	#Summarize each section
	for section in sections:
		if len(section) < 1:
			continue
		section_summary = _get_section_summary(section, mode, frequency_table)
		article_summary += section_summary

	return article_summary


print(_get_file_summary(__FILE_NAME__, 0.75))
