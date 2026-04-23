from retrieval.rag import get_rag_context
from openai import OpenAI
from app.config import OPENAI_API_KEY, BASE_URL, MODEL_NAME

print("✅ SKEPTIC FILE LOADED")

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=BASE_URL   # for OpenRouter
)

def skeptic_agent(query, answer):
    context = get_rag_context(query)

    prompt = f"""
You are a Skeptic AI.

STRICT RULES:
- Challenge EVERY claim
- Check dates, names, "first", "only"
- If no proof → say "NOT VERIFIED"
- Do NOT invent corrections

Context:
{context}

Answer:
{answer}
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