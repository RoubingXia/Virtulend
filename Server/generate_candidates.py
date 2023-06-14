import numpy as np
import json
import openai
from sklearn.metrics.pairwise import cosine_similarity
import os

# Your OpenAI API Key
openai.api_key = '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'

def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    embedding = openai.Embedding.create(input=[text], model=model)["data"][0]["embedding"]
    return np.array(embedding)


def load_embeddings(filename="embeddings.npy"):
    if os.path.exists(filename):
        game_embeddings = np.load(filename)  # load embeddings from the file
        return game_embeddings
    else:
        print("Embedding file does not exist.")
        return None

def generate_candidates(query, games, top_n=10):
    
    query_embedding = get_embedding(query)
    if query_embedding is None:
        return []

    # Load game embeddings from file
    game_ids = list(games.keys())
    game_embeddings = load_embeddings()

    if game_embeddings is None or len(game_embeddings) == 0:
        return []

    # Compute cosine similarity between the query and games' descriptions
    cosine_similarities = cosine_similarity(query_embedding.reshape(1, -1), game_embeddings)

    # Get top_n games that are most similar to the query
    top_game_indices = np.argsort(cosine_similarities[0])[::-1][:top_n]
    candidates = [games[game_ids[i]] for i in top_game_indices]

    return candidates

# Here you need to define your query_embedding and games
# query_embedding = ... 
 # Load the game data
with open("games2.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    games = data

# Then you can call the generate_candidates function
#candidates = generate_candidates("I want games that teach me construction", games, top_n=1)
#print(candidates)