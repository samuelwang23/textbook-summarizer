import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from sentence import Sentence

lines_to_ignore = ["image pop up. Press enter to access the pop up"]

file_name = "WhyEurope.txt"

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

def _get_transition_words():
	return

def _get_symbols():
	return set([".", ",", "|"])


def _get_ineligibles():
	stop_words = set(stopwords.words("english"))
	symbols = _get_symbols()
	return stop_words | symbols

def _split_into_sections(file_contents):
	return file_contents.split("##")

def _get_sentences(section):
    # Tokenize Sentences 
    return [Sentence(text, pos) for pos, text in enumerate(sent_tokenize(section))]

