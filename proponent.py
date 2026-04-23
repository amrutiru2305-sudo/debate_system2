from openai import OpenAI
from app.config import OPENAI_API_KEY, BASE_URL, MODEL_NAME
from retrieval.rag import get_rag_context

client = OpenAI(api_key=OPENAI_API_KEY, base_url=BASE_URL)

def proponent_agent(query):
    context = get_rag_context(query)

    prompt = f"""
You are a Proponent AI.

STRICT RULES:
- Use ONLY the provided context
- Do NOT guess or add new facts
- If info is missing → say "insufficient data"

Context:
{context}

Question: {query}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        extra_headers={
            "HTTP-Referer": "http://localhost",
            "X-Title": "Debate-System"
        }
    )

    return response.choices[0].message.content