# test_movie_microservice.py

import requests

def test_search_by_title():
    url = "http://localhost:8080/movies"
    params = {"title": "Inception"}
    response = requests.get(url, params=params)
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())

def test_search_by_genre():
    # For the genre test, note that my demo expects a TMDb genre ID.
    # For example, the genre ID for Action is 28.
    url = "http://localhost:8080/movies"
    params = {"genre": "28"}
    response = requests.get(url, params=params)
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())

if __name__ == "__main__":
    print("Testing search by title:")
    test_search_by_title()
    print("\nTesting search by genre:")
    test_search_by_genre()
