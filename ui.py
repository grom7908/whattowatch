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
