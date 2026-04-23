import faiss
import numpy as np
from openai import OpenAI
from app.config import OPENAI_API_KEY, BASE_URL

client = OpenAI(api_key=OPENAI_API_KEY, base_url=BASE_URL)

index = faiss.IndexFlatL2(1536)
queries = []
answers = []

def get_embedding(text):
    res = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return np.array(res.data[0].embedding, dtype='float32')

def search_cache(query):
    if not queries:
        return None

    emb = get_embedding(query)
    D, I = index.search(np.array([emb]), 1)

    if D[0][0] < 0.5:
        return answers[I[0][0]]

    return None

def add_to_cache(query, answer):
    emb = get_embedding(query)
    index.add(np.array([emb]))
    queries.append(query)
    answers.append(answer)