# Movie Recommender Application Documentation
## Overview

_The Movie Recommender Application is a Python-based tool that provides movie 
recommendations based on the user's mood. It uses the OMDb API to fetch movie suggestions 
and stores user favorites in a MySQL database. The application features a graphical user 
interface (GUI) built with Tkinter._

## Project Structure
The project consists of the following files:

* main.py: Contains the core logic for interacting with the OMDb API and the MySQL database.
* ui.py: Provides the graphical user interface for the application using Tkinter.

## Core Functionality
1. ### Fetch Movie Recommendations
The application retrieves movie recommendations from the OMDb API based on the user's mood. 
The supported moods and their corresponding genres are:

* Bad: Comedy
* Happy: Adventure
* Sad: Drama
* Angry: Action
* Bored: Documentary
* Excited: Fantasy
* Anxious: Romance

2. ### Save and Retrieve Favorite Movies
Users can add movies to their favorites list and view their saved favorites. The application uses 
a MySQL database to store and manage these favorites. 

## main.py:

```python
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
```

## ui.py:
```python
import tkinter as tk
from tkinter import messagebox
from main import get_recommendations_based_on_mood, add_to_favorite_movies, get_favorite_movies

def show_recommendations():
    mood = mood_entry.get().lower()
    recommendations = get_recommendations_based_on_mood(mood)

    #Display recommendations
    if isinstance(recommendations, str):  #Check if the return value is an error
        messagebox.showerror("Error", recommendations)
    else:
        recommendation_listbox.delete(0, tk.END)  #Clear previous recommendations
        for movie in recommendations:
            recommendation_listbox.insert(tk.END, movie)

def add_favorite():
    selected_movie = recommendation_listbox.get(tk.ACTIVE)
    if selected_movie:
        result = add_to_favorite_movies(selected_movie)  #Save the selected movie
        messagebox.showinfo("Favorite Movies", result)

def show_favorites():
    favorites = get_favorite_movies()
    favorites_listbox.delete(0, tk.END)  #Clear previous favorites
    for movie in favorites:
        favorites_listbox.insert(tk.END, movie)

def main():
    root = tk.Tk()
    root.title("What To Watch")

    #Mood
    tk.Label(root, text="Enter your mood:").pack()
    global mood_entry
    mood_entry = tk.Entry(root)
    mood_entry.pack()

    #Get Recommendations
    tk.Button(root, text="Get Recommendations", command=show_recommendations).pack()

    #Listbox to display recommendations
    global recommendation_listbox
    recommendation_listbox = tk.Listbox(root, height=10, width=50)
    recommendation_listbox.pack()

    #Add to Favorites
    tk.Button(root, text="Add to Favorites", command=add_favorite).pack()

    #Favorites
    tk.Label(root, text="Your Favorite Movies:").pack()
    global favorites_listbox
    favorites_listbox = tk.Listbox(root, height=10, width=50)
    favorites_listbox.pack()

    #Show Favorites
    tk.Button(root, text="Show Favorites", command=show_favorites).pack()

    root.mainloop()

if __name__ == "__main__":
    main()
```

## SQL:
```sql
CREATE DATABASE app_database;

USE app_database;

CREATE TABLE my_favorite_movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    year VARCHAR(10) NOT NULL
);
```

## UI of the project:
![](what_to_watch_img.jpg)

