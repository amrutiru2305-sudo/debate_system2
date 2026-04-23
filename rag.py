from retrieval.search import search_web

def get_rag_context(query):
    return search_web(query)