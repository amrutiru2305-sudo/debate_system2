from flask import Flask, request, jsonify
from agents.proponent import proponent_agent
from agents.skeptic import skeptic_agent
from agents.decomposer import decompose_claims
from agents.moderator import moderator_agent

app = Flask(__name__)


@app.route("/")
def home():
    return "Server is running ✅"
@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    query = data["query"]

    p = proponent_agent(query)
    c = decompose_claims(p)
    s = skeptic_agent(query, p)
    f = moderator_agent(query, p, s, c)

    return jsonify({"result": f})

if __name__ == "__main__":
    app.run(debug=True)