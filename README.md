# 🔍 Financial Semantic Search Engine ("Mini-Google")

A Production-Grade Semantic Search Engine designed to move beyond keyword matching. This project uses **Natural Language Processing (NLP)** and **Vector Databases** to find financial news based on "meaning" and context.

## 🚀 The Core Innovation
Traditional search looks for exact words. If you search for "economic downturn," a traditional engine might miss an article titled "Recession looms as GDP falls." 

**This engine understands they are the same concept.**

## 🏗️ System Architecture
The project follows a decoupled architecture to ensure scalability and low latency:

1.  **Ingestion Pipeline**: Fetches live data via MarketAux API, generates 384-dimensional embeddings using `sentence-transformers`, and indexes them in a **FAISS** vector vault.
2.  **Search Service**: A **FastAPI** backend that converts user queries into vectors in real-time and performs sub-millisecond similarity lookups.
3.  **Frontend**: A responsive, Google-inspired interface for a seamless user experience.

## 🛠️ Tech Stack
- **Language**: Python 3.11
- **ML Frameworks**: Sentence-Transformers (BERT-based `all-MiniLM-L6-v2`)
- **Vector Database**: FAISS (Facebook AI Similarity Search)
- **API Framework**: FastAPI (Asynchronous Python)
- **Data Source**: MarketAux Financial API
- **DevOps**: Git, GitHub

## 📂 Project Structure
```text
Semantic-Search-Engine/
├── data/               # Local storage for Vector Index & CSV Metadata
├── scripts/
│   ├── ingest.py       # Data Pipeline: Fetch -> Embed -> Index
│   └── search.py       # Logic: Vector Similarity Search
├── main.py             # FastAPI Server Entry Point
├── index.html          # Web Frontend
└── requirements.txt    # Project Dependencies
