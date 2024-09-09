# Movie Recommender Application

## Overview

The Movie Recommender Application is a Python-based desktop application built with Tkinter. It offers movie recommendations based on user mood and allows users to save and view their favorite movies. The application integrates with the OMDb API for movie recommendations and uses MySQL for managing favorite movies.

## Components

### '''import mysql.connector
import requests

#MySQL connection details
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '7908',
    'database': 'movie_app'
}

#Function to connect to the MySQL database
def connect_db():
    return mysql.connector.connect(**db_config)

#Function to fetch movie recommendations using the OMDb API
def get_movie_recommendations(keyword):
    api_key = '7b368d97'
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
            "INSERT INTO favorite_movies (title, year) VALUES (%s, %s)",
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
'''

- **Purpose**: Contains core functionality for interacting with the OMDb API and MySQL database.
- **Key Functions**:
  - `connect_db()`: Connects to the MySQL database using the provided configuration.
  - `get_movie_recommendations(keyword)`: Fetches movie recommendations from the OMDb API based on the provided keyword.
  - `save_to_favorites(movie)`: Saves a movie to the MySQL database.
  - `get_favorite_movies()`: Retrieves favorite movies from the MySQL database.
  - `mood_response(mood)`: Provides movie recommendations based on the user's mood.

### `ui.py`

- **Purpose**: Provides the Tkinter-based graphical user interface (GUI) for interacting with the movie recommender.
- **Key Functions**:
  - `show_recommendations()`: Fetches and displays movie recommendations based on user input.
  - `add_favorite()`: Adds the selected movie from the recommendations list to the favorites list.
  - `show_favorites()`: Displays the list of favorite movies stored in the MySQL database.

## MySQL Database Configuration

- **Database Name**: `movie_app`
- **Table Name**: `favorite_movies`
- **Table Schema**:
  - `id`: INT, AUTO_INCREMENT, PRIMARY KEY
  - `title`: VARCHAR(255), NOT NULL
  - `year`: VARCHAR(10), NOT NULL

## API Integration

- **API Used**: OMDb API
- **API Key**: `7b368d97`
- **API Endpoint**: `http://www.omdbapi.com/?apikey={api_key}&s={keyword}`

## Setup

1. **Install Required Packages**: Ensure `mysql-connector-python`, `requests`, and `tkinter` are installed.
2. **Database Setup**: Create a MySQL database named `movie_app` and a table named `favorite_movies` using the provided schema.
3. **Configuration**: Update MySQL connection details and API key in `main.py` as needed.

## Usage

1. **Run the Application**: Execute `ui.py` to start the Tkinter GUI.
2. **Get Recommendations**: Enter a mood in the provided entry field and click "Get Recommendations" to view movie suggestions.
3. **Add to Favorites**: Select a movie from the recommendations list and click "Add to Favorites" to save it to the database.
4. **View Favorites**: Click "Show Favorites" to display saved movies from the MySQL database.

## Troubleshooting

- **RecursionError**: Check for any recursive function calls in `main.py`. Ensure no function is calling itself indefinitely.
- **Connection Issues**: Verify that MySQL server is running and connection details are correct.
- **API Errors**: Ensure the OMDb API key is valid and check for network issues.

For additional help, consult relevant documentation for the OMDb API, MySQL, or Python libraries used.

