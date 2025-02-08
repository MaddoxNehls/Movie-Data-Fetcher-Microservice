from flask import Flask, request, jsonify, abort
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get API key from environment variable
TMDB_API_KEY = os.getenv("TEST_API_KEY")
if not TMDB_API_KEY:
    raise ValueError("API key is missing! Set TEST_API_KEY in the .env file.")

# TMDb search endpoint (for title-based search)
TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
# TMDb discover endpoint for genre-based searches
TMDB_DISCOVER_URL = "https://api.themoviedb.org/3/discover/movie"

def get_movies_by_title(title):
    """Call TMDb API to search for movies by title."""
    params = {
        'api_key': TMDB_API_KEY,
        'query': title
    }
    response = requests.get(TMDB_SEARCH_URL, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []

def get_movies_by_genre(genre):
    """Call TMDb API to search for movies by genre."""
    params = {
        'api_key': TMDB_API_KEY,
        'with_genres': genre
    }
    response = requests.get(TMDB_DISCOVER_URL, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []

@app.route('/movies', methods=['GET'])
def movies():
    title = request.args.get('title')
    genre = request.args.get('genre')

    if title:
        results = get_movies_by_title(title)
        if not results:
            abort(404, description="Movie not found")
        return jsonify(results)
    elif genre:
        results = get_movies_by_genre(genre)
        if not results:
            abort(404, description="Movie not found")
        return jsonify(results)
    else:
        abort(400, description="Invalid request. Provide either a 'title' or 'genre' query parameter.")

@app.errorhandler(404)
def handle_404(error):
    return jsonify(error=str(error)), 404

@app.errorhandler(400)
def handle_400(error):
    return jsonify(error=str(error)), 400

if __name__ == '__main__':
    app.run(debug=True, port=8080)
