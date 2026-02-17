import faiss
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

class FinancialSearchEngine:
    def __init__(self):
        # Using the same model as ingestion
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        # Load our saved data from the data folder
        self.df = pd.read_csv("data/news_vault.csv")
        self.index = faiss.read_index("data/vector_index.faiss")

    # Ensure this is named 'search' to match main.py
    def search(self, query, top_k=3):
        # 1. Convert user query to a vector
        query_vector = self.model.encode([query]).astype('float32')
        
        # 2. Find the top K closest matches
        distances, indices = self.index.search(query_vector, k=top_k)
        
        # 3. Retrieve results from the dataframe
        results = self.df.iloc[indices[0]].to_dict(orient='records')
        return results