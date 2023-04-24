import hnswlib
from sentence_transformers import SentenceTransformer
import numpy as np
import json
from datetime import datetime
from utils.logger import Logger
from utils.parser import Parser
from database.vector_db_helper import vectorDbHelper

# Create a logger instance with the name "memory"
logger = Logger("memory")


class Memory:
    def __init__(
        self,
        index_path="tuning_data/vectordb/memories.bin",
        model_name="paraphrase-distilroberta-base-v2",
    ):
        self.index_path = index_path
        self.vectorDbHelper = vectorDbHelper()
        self.model = SentenceTransformer(model_name)
        self.dim = self.model.get_sentence_embedding_dimension()
        self.index = hnswlib.Index(space="cosine", dim=self.dim)
        # Load your text data into a list or numpy array
        logger.info("Memory implantation...")
        self.load_memories()
        self._load_index()
        logger.info("...Memory implanted")

    def _load_index(self):
        try:
            self.index.load_index(self.index_path)
        except (RuntimeError, FileNotFoundError):
            logger.info(
                f"No existing index found at {self.index_path}. Initializing new index with default vectors."
            )
            self._initialize_index()

    def _initialize_index(self):
        normalizedText = []
        # Generate embeddings for your text data
        for memory in self.memories:
            normalized_embedding = self.vectorDbHelper.text_to_normalized_vector(
                memory["text"]
            )
            normalizedText.append(normalized_embedding)
        # Set up the HNSW index
        num_elements = 5000  # number of embeddings
        # ef_construction controls the trade-off between index build time and quality of the index. It sets the size of the dynamic list of candidate neighbors that each node maintains during the index construction process. Increasing ef_construction will lead to better recall at the cost of longer index build time.
        # M is the number of bi-directional links created for each new element during the index construction process. Increasing M will lead to better recall but also higher memory usage and slower index construction.
        self.index.init_index(max_elements=num_elements, ef_construction=500, M=240)
        # The value ef passed to index.set_ef(ef) represents the maximum number of elements to be visited during the search for each query. So, a higher value of ef means that more elements will be visited during the search, which can lead to better search results but can also increase the search time.
        self.index.set_ef(200)
        # Index the embeddings
        self.index.add_items(normalizedText)

        # Save the index to disk
        self.index.save_index(self.index_path)

    def query_index(self, query_text):
        # Encode the query text
        normalized_query_vec = self.vectorDbHelper.text_to_normalized_vector(query_text)
        results = self.extract_text_from_index(query_text, normalized_query_vec)
        return results

    def extract_text_from_index(
        self, query_text, normalized_query_vec, threshold_distance=0.78
    ):
        # Find the nearest neighbors
        num_results = min(4, len(query_text))
        labels, distances = self.index.knn_query(normalized_query_vec, k=num_results)

        # Filter by distance threshold
        relevant_indices = np.where(distances <= threshold_distance)[0]

        # Return the corresponding text data and distances
        results = []
        validMemoriesIndexes = relevant_indices.tolist()

        for i in validMemoriesIndexes:
            results.append(
                {"memory": self.memories[labels[0][i]], "distance": distances[0][i]}
            )
        return results

    def add_elements_to_index(self, new_text_data, tag, json=None):
        # Check if the new memory already exists in the memories list
        results = self.query_index(new_text_data)
        for result in results:
            if result["distance"] <= 0.2:
                logger.info(
                    f"Memory '{new_text_data}' is too similar to another memory"
                )
                return

        logger.info("implant a new memory...")
        # Generate embeddings for the new text data
        normalize_vec = self.vectorDbHelper.text_to_normalized_vector(new_text_data)

        # Create a new memory object with current timestamp
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        new_memory = {"text": new_text_data, "timestamp": now, "tag": tag}

        logger.info("new memory to implant: " + new_memory["text"])
        # Append the new memory to the memories list
        self.memories.append(new_memory)
        # Add the new embeddings to the index
        self.index.add_items(normalize_vec)

        # Save the updated index to disk
        self.index.save_index(self.index_path)
        self.save_memories()
        logger.info("...memory implanted")

    def load_memories(self):
        with open("tuning_data/memories.json", "r") as f:
            self.memories = json.load(f)

    def save_memories(self):
        with open("tuning_data/memories.json", "w") as f:
            json.dump(self.memories, f)
