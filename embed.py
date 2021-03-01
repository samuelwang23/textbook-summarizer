import numpy as np
from gensim.models import Word2Vec

class Embedder:
    def __init__(self, w2v):
        self.w2v = w2v
        return

    def _embed_sentence(self, sentence, length):
        vector = np.sort([ self.w2v[word] for word in sentence.tokens])[0:length]
        if vector.shape[0] < length:
            zeros = np.zeros((length - vector.shape[0], vector.shape[1]))
            vector = np.concatenate((vector, zeros))
        return vector
        
    def _embed_sentences(self, sentences, length):
        return np.array([ self._embed_sentence(sentence, length)
        for sentence in sentences])