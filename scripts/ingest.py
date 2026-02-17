import requests
import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os

# 1. Configuration - Senior engineers keep constants at the top
API_TOKEN = "Qlmb1fOVH6iY2u5rvCq1QNEd1DQuFvMBerKbCQHZ" 
DATA_DIR = "data"
CSV_PATH = os.path.join(DATA_DIR, "news_vault.csv")
INDEX_PATH = os.path.join(DATA_DIR, "vector_index.faiss")

def fetch_financial_news():
    print("📡 Step 1: Fetching live financial news...")
    url = f"https://api.marketaux.com/v1/news/all?language=en&api_token={API_TOKEN}"
    try:
        response = requests.get(url)
        response.raise_for_status() # Check for API errors
        data = response.json().get('data', [])
        return pd.DataFrame(data)[['title', 'description', 'url', 'published_at']]
    except Exception as e:
        print(f"❌ API Error: {e}")
        return None

def build_vector_vault(df):
    print("🧠 Step 2: Vectorizing text (this may take a moment)...")
    # This model turns text into 384-dimensional vectors
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Combine title and description for richer "meaning"
    text_data = (df['title'] + " " + df['description'].fillna('')).tolist()
    embeddings = model.encode(text_data)
    
    # 3. Create the FAISS Index (The 'Search Engine' part)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype('float32'))
    
    # 4. Save everything to the /data folder
    faiss.write_index(index, INDEX_PATH)
    df.to_csv(CSV_PATH, index=False)
    print(f"✅ Success! Saved {len(df)} articles to {CSV_PATH}")
    print(f"✅ Success! Saved vector index to {INDEX_PATH}")

if __name__ == "__main__":
    # Ensure the data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    news_df = fetch_financial_news()
    if news_df is not None and not news_df.empty:
        build_vector_vault(news_df)
    else:
        print("⚠️ No data found. Check your API key or connection.")