import openai
import json
import numpy as np

# Your OpenAI API Key
openai.api_key = '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'

def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    embedding = openai.Embedding.create(input=[text], model=model)["data"][0]["embedding"]
    return np.array(embedding)

def generate_embeddings(games, model="text-embedding-ada-002", filename="embeddings.npy"):
    game_ids = list(games.keys())
    game_embeddings = [get_embedding(games[game_id]["detailed_description"]) for game_id in game_ids if games[game_id].get("detailed_description")]
    np.save(filename, game_embeddings) # save embeddings to a file

 # Load the game data
with open("games2.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    games = data

# Generate and save embeddings for all games
generate_embeddings(games)
