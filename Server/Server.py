from flask import Flask, request, jsonify
from Recommendation import *

app = Flask(__name__)

@app.route('/recommendation', methods=['POST'])
def get_recommendations():
    # Get the input context from the request
    user_query = request.json.get('context')

    # Load the game data
    with open("games2.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        games = data
    candidates = fake_generate_candidates(user_query, games, top_n=3)
    #ranked_order = ranker(candidates, user_query)

    fake_response_context = candidates

    # Return the response context as JSON
    return jsonify({'response': fake_response_context})

if __name__ == '__main__':
    app.run()
