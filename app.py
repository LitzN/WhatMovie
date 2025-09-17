import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search")
def search():
    query = request.args.get("q")
    if not query:
        return "Please provide a search query (?q=movie)", 400

    url = f"{BASE_URL}/search/movie?api_key={TMDB_API_KEY}&query={query}"
    response = requests.get(url)
    data = response.json()

    movies = []
    for movie in data.get("results", []):
        poster = None
        if movie.get("poster_path"):
            poster = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
        movies.append({
            "title": movie["title"],
            "release_date": movie.get("release_date"),
            "poster": poster
        })

    return render_template("results.html", movies=movies, query=query)

