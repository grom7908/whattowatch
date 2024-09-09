import mysql.connector
import requests

#MySQL connection details
db_config = {
    'host': 'host',
    'user': 'username',
    'password': 'your_password',
    'database': 'whattowatch_app'
}

#Function to connect to the MySQL database
def connect_db():
    return mysql.connector.connect(**db_config)

#Function to fetch movie recommendations using the OMDb API
def get_movie_recommendations(keyword):
    api_key = 'your_api_key'
    url = f"http://www.omdbapi.com/?apikey={api_key}&s={keyword}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get('Response') == 'True':
            movies = data.get('Search', [])
            movie_list = [f"{movie.get('Title')} ({movie.get('Year')})" for movie in movies]
            return movie_list
        else:
            return f"No movies found for the genre: {keyword}"
    else:
        return "Error connecting to the OMDb API."

#Function to save a movie to the favorites in MySQL
def save_to_favorites(movie):
    db = connect_db()
    cursor = db.cursor()

    #Split movie into title and year
    title, year = movie.rsplit('(', 1)
    year = year.strip(')')

    try:
        cursor.execute(
            "INSERT INTO my_favorite_movies (title, year) VALUES (%s, %s)",
            (title.strip(), year)
        )
        db.commit()
        return f"{title.strip()} has been added to your favorites!"
    except mysql.connector.Error as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        db.close()

#Function to retrieve favorite movies from the MySQL database
def fetch_favorite_movies():
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("SELECT title, year FROM favorite_movies")
    results = cursor.fetchall()

    favorite_movies = [f"{row[0]} ({row[1]})" for row in results]

    cursor.close()
    db.close()

    return favorite_movies

#Function to respond to user mood and provide movie recommendations
def mood_response(mood):
    if "bad" in mood:
        return get_movie_recommendations('comedy')
    elif "happy" in mood:
        return get_movie_recommendations('adventure')
    elif "sad" in mood:
        return get_movie_recommendations('drama')
    elif "angry" in mood:
        return get_movie_recommendations('action')
    elif "bored" in mood:
        return get_movie_recommendations('documentary')
    elif "excited" in mood:
        return get_movie_recommendations('fantasy')
    elif "anxious" in mood:
        return get_movie_recommendations('romance')
    else:
        return "Invalid mood."

#Main function to interact with Tkinter
def get_recommendations_based_on_mood(mood):
    return mood_response(mood)

#Function to add a movie to favorites
def add_to_favorite_movies(movie):
    return save_to_favorites(movie)

#Function to get favorite movies
def get_favorite_movies():
    return fetch_favorite_movies()
