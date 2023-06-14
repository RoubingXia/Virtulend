from flask import Flask, request, jsonify
from generate_candidates import *

app = Flask(__name__)


@app.route('/recommendation', methods=['POST'])
def get_recommendations():
    # Get the input context from the request
    user_query = request.json.get('context')

    # Load the game data
    with open("games2.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        games = data
    candidates = generate_candidates(user_query, games, top_n=3)
    response_context = candidates

    # Return the response context as JSON
    return jsonify({'response': response_context})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
