from tabulate import tabulate
import numpy as np
import json
import openai
from sklearn.metrics.pairwise import cosine_similarity
import os

# Your OpenAI API Key
openai.api_key = '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'

def generate_game_embeddings(games, model="text-embedding-ada-002", filename="embeddings.npy"):
    game_ids = list(games.keys())
    game_embeddings = [get_embedding(games[game_id]["detailed_description"]) for game_id in game_ids if games[game_id].get("detailed_description")]
    np.save(filename, game_embeddings) # save embeddings to a file


def format_games(games):
    # convert the game data into a string format
    formatted_games = '\n'.join([f'index: {i}, name: {game["name"]}, detailed_description: {game["detailed_description"]}' for i, game in enumerate(games)])
    return formatted_games

# Function to rank games
def ranker(games, user_query):
    system_message = {"role": "system", "content": "You are RankGPT, an intelligent assistant that can rank games based on how helpful they would be to the user."}
    context_string = format_games(games)

    prompt = f"""
    I will provide you with {len(games)} games, each indicated by number `index` field.
    Rank the games based on their relevance to query: {user_query}.

    {context_string}

    Search Query: {user_query}.
    
    Rank the {len(games)} games above based on their relevance to the search query.
    Use all the information available to you to rank the games.
    The games should be listed in descending order using identifiers. 
    The most relevant games should be listed first. If multiple games are equally relevant, use the number of positive votes as a tie-breaker.
    The output format should be a list of identifiers, separated by commas and enclosed in square brackets.
    Only output the list of identifiers, do not output any other text.
    """

    modified_user_message = {'role': 'user', 'content': prompt}

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[system_message, modified_user_message],
        stream = False,
        temperature=0.7,
    )

    ranked_order = json.loads(response.choices[0].message.content)

    return ranked_order

def load_embeddings(filename="embeddings.npy"):
    if os.path.exists(filename):
        game_embeddings = np.load(filename)  # load embeddings from the file
        return game_embeddings
    else:
        print("Embedding file does not exist.")
        return None

def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    embedding = openai.Embedding.create(input=[text], model=model)["data"][0]["embedding"]
    return np.array(embedding)


def generate_candidates(query, games, top_n=10):
    # Embed the query and games' descriptions
    query_embedding = get_embedding(query)
    if query_embedding is None:
        return []

    game_ids = list(games.keys())
    game_embeddings = load_embeddings()
    if game_embeddings is None:
        generate_game_embeddings(games)
        game_embeddings = load_embeddings()
    if len(game_embeddings) == 0:
        return []

    # Compute cosine similarity between the query and games' descriptions
    cosine_similarities = cosine_similarity(query_embedding.reshape(1, -1), game_embeddings)

    # Get top_n games that are most similar to the query
    top_game_indices = np.argsort(cosine_similarities)[0][::-1][:top_n]
    candidates = [games[game_ids[i]] for i in top_game_indices]

    return candidates


def generate_candidates_summary(query, games, top_n=10):
    # Embed the query and games' descriptions
    query_embedding = get_embedding(query)
    if query_embedding is None:
        return []

    game_ids = list(games.keys())
    game_embeddings = load_embeddings()
    if game_embeddings is None:
        generate_game_embeddings(games)
        game_embeddings = load_embeddings()
    if len(game_embeddings) == 0:
        return []

    # Compute cosine similarity between the query and games' descriptions
    cosine_similarities = cosine_similarity(query_embedding.reshape(1, -1), game_embeddings)

    # Get top_n games that are most similar to the query
    top_game_indices = np.argsort(cosine_similarities)[0][::-1][:top_n]
    candidates = [games[game_ids[i]] for i in top_game_indices]
    table_data = []
    headers = ["Game", "Price"]
    for game in candidates:
        game_name = game["name"]
        game_price = game["price"]
        table_data.append([game_name, game_price])
    return table_data

def fake_generate_candidates(query, games, top_n=10):
    game_ids = list(games.keys())
    candidates = [games[game_ids[i]] for i in range(1,3)]
    return candidates


def print_game_table(games):
    table_data = []
    headers = ["Game", "Price"]

    for game in games:
        game_name = game["name"]
        game_price = game["price"]
        table_data.append([game_name, game_price])

    print(tabulate(table_data, headers=headers, tablefmt="grid"))


# In[ ]:




