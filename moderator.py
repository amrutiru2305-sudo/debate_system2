from retrieval.rag import get_rag_context
from openai import OpenAI
from app.config import OPENAI_API_KEY, BASE_URL, MODEL_NAME

# ✅ DEFINE CLIENT
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=BASE_URL
)

def moderator_agent(query, proponent, skeptic, claims):
    context = get_rag_context(query)

    prompt = f"""
You are a Moderator AI.

STRICT RULES:
- Use ONLY context as ground truth
- Do NOT modify facts without evidence
- If unsure → mark UNCERTAIN
- Never assume

Context:
{context}

Claims:
{claims}

Output EXACT format:

Claims Evaluation:
1. <claim> → CORRECT / INCORRECT / UNCERTAIN → Evidence: ...
2. ...

Final Answer: ...
Confidence: ...%
Hallucination Risk: LOW / MEDIUM / HIGH
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