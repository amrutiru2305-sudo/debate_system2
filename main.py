from evaluation.metrics import evaluate_claims

def run_system(query):
    print("\n🔹 USER QUERY:", query)

    cached = search_cache(query)
    if cached:
        print("\n⚡ Cache Hit:\n", cached)
        return

    proponent = proponent_agent(query)
    print("\n🟢 Proponent:\n", proponent)

    claims = decompose_claims(proponent)
    print("\n🔍 Claims:\n", claims)

    skeptic = skeptic_agent(query, proponent)
    print("\n🔴 Skeptic:\n", skeptic)

    final = moderator_agent(query, proponent, skeptic, claims)
    print("\n🧑‍⚖️ Final Verdict:\n", final)

    # 🔥 Evaluation
    metrics = evaluate_claims(final)
    print("\n📊 Metrics:")
    print("Accuracy:", metrics["accuracy"])
    print("Hallucination Rate:", metrics["hallucination_rate"])

    add_to_cache(query, final)