import hnswlib
from sentence_transformers import SentenceTransformer
import numpy as np
import json
from datetime import datetime
from utils.logger import Logger


# Create a logger instance with the name "memory"
logger = Logger("vectorDbHelper")


class vectorDbHelper:
    def __init__(self, model_name="paraphrase-distilroberta-base-v2"):
        self.model = SentenceTransformer(model_name)
        self.dim = self.model.get_sentence_embedding_dimension()

    def text_to_normalized_vector(self, query_text):
        query_vec = self.model.encode([query_text])[0]
        normalized_query_vec = query_vec / np.linalg.norm(query_vec)

        return normalized_query_vec
