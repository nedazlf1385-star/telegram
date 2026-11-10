import requests

def get_movie_info_by_id(movie_id):
    url = f'https://moviesapi.ir/api/v1/movies/{movie_id}'
    response = requests.get(url)
    if response.status_code != 200:
        return 'ERROR'
    else:
        response = response.json()
        title = response['title']
        country = response['country']
        director = response['director']
        year = response['year']
        imdb_rate = response['imdb_rating']

        return (title, country , director, year, imdb_rate)


API_KEY = "8f219780"

def search_movie_by_title(movie_name):
    url = "https://www.omdbapi.com/"

    params = {
        "apikey": API_KEY,
        "t": movie_name,
        "plot": "full"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("Response") == "False":
            return None

        return {
            "title": data.get("Title", "نامشخص"),
            "year": data.get("Year", "نامشخص"),
            "country": data.get("Country", "نامشخص"),
            "director": data.get("Director", "نامشخص"),
            "rating": data.get("imdbRating", "نامشخص"),
            "genre": data.get("Genre", "نامشخص"),
            "plot": data.get("Plot", "توضیحی ثبت نشده"),
            "poster": data.get("Poster"),
            "actors": data.get("Actors", "نامشخص"),
            "runtime": data.get("Runtime", "نامشخص")
        }

    except requests.RequestException:
        return None
