from flask import Flask
from flask import request, json
from flask_cors import CORS, cross_origin
import os, random
from cluster_summarizer import summarize
from consts import __CLUSTER_TYPES__
import pandas as pd
import json

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
	return file_contents.replace(" . . .", "")

@app.route('/')
def hello_world():
    return "Hello There!"

@app.route('/api/v1/random_test', methods=['GET'])
@cross_origin()
def get_random_test():
    results = {}
    results["path"] = get_random_text()
    results["text"] = _get_file_contents(results["path"])
    while len(results["text"]) > 2700 or len(results["text"]) < 1300:
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

@app.route('/api/v1/reviews', methods=['POST'])
def post_reviews():
    review_json = request.args.get('review')
    if review_json:
        reviews = pd.read_csv('/home/swang/TextSummarizer/reviews.csv')

        review = pd.read_json(review_json, typ='series', orient='records')

        reviews = reviews.append(review, ignore_index=True)

        reviews.to_csv("/home/swang/TextSummarizer/reviews.csv", header = True, index = False)
        return "The review was added."

    return "Your request was not valid. Please try again."

@app.route('/api/v1/summarize', methods=['POST'])
def get_summary():
    text = request.form.get('text')
    cluster_type = request.form.get('cluster_type')
    if text and cluster_type:
        results = {}
        results["summary"] = summarize(text, cluster_type)
        return json.dumps(results)
    return "Your request was not valid. Please try again."
