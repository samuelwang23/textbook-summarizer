from flask import Flask
from flask import request, json
from flask_cors import CORS, cross_origin
import os, random
from cluster_summarizer import summarize
from consts import __CLUSTER_TYPES__

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def _get_file_contents(file_name):
	file_contents = ""
	file = open(file_name, "r", encoding='cp1252')
	while(True):
		line = file.readline()
		if not line:
			break
		else:
			file_contents += line
	return file_contents

@app.route('/')
def hello_world():
    return "Hello There!"

@app.route('/api/v1/random_test', methods=['GET'])
@cross_origin()
def get_random_test():
    results = {}
    results["path"] = get_random_text()
    results["text"] = _get_file_contents(results["path"])
    results["cluster_type_1"] = random.choice(__CLUSTER_TYPES__)
    results["summary_1"] = summarize(results["text"], results["cluster_type_1"])
    results["cluster_type_2"] = random.choice(__CLUSTER_TYPES__)
    while results["cluster_type_2"] == results["cluster_type_1"]:
        results["cluster_type_2"] = random.choice(__CLUSTER_TYPES__)
    results["summary_2"] = summarize(results["text"], results["cluster_type_2"])
    return json.dumps(results)


def get_random_text():
    parent_path = "/home/swang/TextSummarizer/static/Sections"
    random_chapter_path = os.path.join(parent_path, random.choice(os.listdir(parent_path)))
    return os.path.join(random_chapter_path, random.choice(os.listdir(random_chapter_path)))
