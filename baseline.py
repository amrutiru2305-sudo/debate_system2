from openai import OpenAI
from app.config import OPENAI_API_KEY, BASE_URL, MODEL_NAME

client = OpenAI(api_key=OPENAI_API_KEY, base_url=BASE_URL)

def baseline_agent(query):
    prompt = f"""
Answer the question directly.

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