import tmdbsimple as tmdb

tmdb.API_KEY = ''

def search_movie(movie_name, year):
    search = tmdb.Search()
    response = search.movie(query=movie_name)
    most_popular_movie_id = None
    highest_popularity = -1
    for movie in response['results']:
        # Ensure the movie has a release date before comparing its year
        if 'release_date' in movie and movie['release_date'][:4] == year:
            if movie['popularity'] > highest_popularity:
                highest_popularity = movie['popularity']
                most_popular_movie_id = movie['id']

    return most_popular_movie_id

def get_movie_connections(movie_id):
    movie = tmdb.Movies(movie_id)
    credits = movie.credits()
    actors = credits['cast'][:10]  # Limit to top 10 actors for simplicity
    directors = [person for person in credits['crew'] if person['job'] == 'Director']

    return [person['name'] for person in actors + directors]

def get_connecting_movies(name):
    search = tmdb.Search()
    response = search.person(query=name)
    if not response['results']:
        return []
    person_id = response['results'][0]['id']
    person = tmdb.People(person_id)
    credits = person.movie_credits()['cast']

    connecting_movies = []
    i = 0
    for credit in credits:  # Limit to first 7 movies
        if credit.get('popularity', 0) > 8:  # Ensure popularity is a key and set a default
            connecting_movies.append(f"{name} - {credit['title']} ({credit['release_date'][:4]})")
            i += 1
            if i == 7:
                break
    return connecting_movies

def main():
    print("Enter Movie Name and Year (e.g., Inception 2010): ")
    user_input = input()
    for _ in range(25):
            print()
    if len(user_input) < 5 or not user_input[-5].isspace():  # Basic check for format
        print("Invalid format. Please enter the movie name followed by the year.")
        return

    movie_name, year = user_input[:-5].strip(), user_input[-4:]
    movie_id = search_movie(movie_name, year)
    if not movie_id:
        print("Movie not found.")
        return

    connections = get_movie_connections(movie_id)
    if not connections:
        print("No connections found for this movie.")
        return

    print("\nConnecting Movies:")
    for name in connections:
        connecting_movies = get_connecting_movies(name)
        for movie in connecting_movies:
            print(movie)

while True:
    if __name__ == "__main__":
        try:
            main()
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
