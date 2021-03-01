import pandas as pd
from helpers import _get_file_contents, _get_sentences
import importlib

# Plotting Imports
import matplotlib.pyplot as plt
import seaborn as sns

# Embedding Imports
from embed import Embedder
from gensim.models import Word2Vec

# Dimension Imports
from sklearn.manifold import TSNE
from dimensions import DimensionReducer

# Clustering Imports
cluster_module = importlib.import_module("sklearn.cluster")

# Scoring Imports
from scorer import FrequencyScorer

# Summary Imports
from summary import Summarizer


def _get_tokens_of_sentences(sentences):
    return [sentence.tokens for sentence in sentences]


def _plot_clusters(reduction, clustering):
    reduction["c"] = clustering
    plt.figure(figsize=(16,10))
    color_count = len(set(clustering))

    sns.scatterplot(
        x=reduction["x"], y=reduction["y"],
        hue="c",
        palette=sns.color_palette("hls", color_count),
        data=reduction,
        legend="full",
        alpha=1
    )

def summarize(file_contents, cluster_type):
    sentences = _get_sentences(file_contents)

    model = Word2Vec(_get_tokens_of_sentences(sentences), min_count=1)

    embedder = Embedder(model)

    embeddings = embedder._embed_sentences(sentences, 8)

    embeddings = embeddings.reshape((len(sentences), embeddings.shape[1] * embeddings.shape[2]))

    reducer = TSNE(n_components=2, perplexity=40, n_iter=300)

    reduction = pd.DataFrame(DimensionReducer(reducer).reduce(embeddings), columns=["x", "y"]).round(0)

    clusterer = getattr(cluster_module, cluster_type)
    clustering = clusterer().fit_predict(reduction)

    clusters = dict()
    for pos, cluster in enumerate(clustering):
        if cluster in clusters:
            clusters[cluster].append(sentences[pos])
        else:
            clusters[cluster] = [sentences[pos]]

    Scorer =  FrequencyScorer(file_contents)

    summary = []

    for cluster in sorted(clusters.keys()):
        scores = Scorer._get_scores(clusters[cluster])
        cluster_summary = Summarizer(scores, 1)
        summary = summary + cluster_summary.summary

    summary_text = ""
    for sentence in summary:
        summary_text += sentence.text + " "
    print(summary_text)
