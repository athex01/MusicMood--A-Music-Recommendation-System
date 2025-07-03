import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser
from recommendation_engine import recommend_songs, label_encoders

# GUI Application
def handle_recommendation():
    """Handle user input and display recommendations."""
    genre = genre_combobox.get().strip()
    mood = mood_combobox.get().strip()
    language = language_combobox.get().strip()
    age = age_combobox.get().strip()

    recommendations = recommend_songs(genre, mood, language, age)
    if isinstance(recommendations, str):  # If error message
        messagebox.showerror("Error", recommendations)
    else:
        result_label.config(text="\n".join(f"\u2022 {song}" for song in recommendations))
        save_button.config(state="normal")
        youtube_button.config(state="normal")
        spotify_button.config(state="normal")
        apple_music_button.config(state="normal")

def open_search(song, platform):
    """Open search on the selected platform."""
    query = song.replace(' ', '+')

    if platform == "YouTube":
        url = f"https://www.youtube.com/results?search_query={query}"
    elif platform == "Spotify":
        url = f"https://open.spotify.com/search/{query}"
    elif platform == "Apple Music":
        url = f"https://music.apple.com/us/search?term={query}"
    else:
        url = None

    if url:
        webbrowser.open(url)
    else:
        messagebox.showerror("Error", "Invalid platform selected.")

def save_recommendations():
    """Save recommendations to a file."""
    with open("recommendations.txt", "w") as f:
        f.write(result_label.cget("text"))
    messagebox.showinfo("Saved", "Recommendations saved to 'recommendations.txt'.")

# Build GUI
root = tk.Tk()
root.title("♫⋆ Music Recommendation System by Kshitij ♫⋆")
root.geometry("500x650")
root.configure(bg="lavender")

# Header Label
header_label = ttk.Label(root, text="♫⋆ Music Recommendation System by Kshitij ♫⋆", font=("Helvetica", 15, "bold"), background="#e0f7fa", foreground="#00796b")
header_label.pack(pady=20)
header_label = ttk.Label(root, text="Fill the details", font=("Helvetica", 15, "bold"), background="#e0f7fa", foreground="#00796b")
header_label.pack(pady=20)

# Card Frame
card_frame = ttk.Frame(root, padding=20, style="TFrame")
card_frame.place(relx=0.5, rely=0.5, anchor="center")

style = ttk.Style()
style.configure("TFrame", background="#ffffff", borderwidth=3, relief="solid")
style.configure("TLabel", font=("Helvetica", 12), background="#ffffff", foreground="black")
style.configure("TButton", font=("Helvetica", 12), background="black", foreground="black")

# Genre Dropdown
ttk.Label(card_frame, text="Genre:").grid(row=0, column=0, sticky="w", pady=5)
genre_combobox = ttk.Combobox(card_frame, values=sorted(label_encoders['Genre'].classes_), state="readonly")
genre_combobox.grid(row=0, column=1, pady=5)

# Mood Dropdown
ttk.Label(card_frame, text="Mood:").grid(row=1, column=0, sticky="w", pady=5)
mood_combobox = ttk.Combobox(card_frame, values=sorted(label_encoders['Mood'].classes_), state="readonly")
mood_combobox.grid(row=1, column=1, pady=5)

# Language Dropdown
ttk.Label(card_frame, text="Language:").grid(row=2, column=0, sticky="w", pady=5)
language_combobox = ttk.Combobox(card_frame, values=sorted(label_encoders['Language'].classes_), state="readonly")
language_combobox.grid(row=2, column=1, pady=5)

# Age Dropdown
ttk.Label(card_frame, text="Age:").grid(row=3, column=0, sticky="w", pady=5)
age_combobox = ttk.Combobox(card_frame, values=sorted(label_encoders['Age'].classes_), state="readonly")
age_combobox.grid(row=3, column=1, pady=5)

# Recommendation Button
recommend_button = ttk.Button(card_frame, text="Get Recommendations", command=handle_recommendation)
recommend_button.grid(row=4, column=0, columnspan=2, pady=10)

# Result Label
result_label = ttk.Label(card_frame, text="", font=("Helvetica", 14, "italic"), foreground="blue", background="#ffffff")
result_label.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")

# Search Buttons
youtube_button = ttk.Button(card_frame, text="Search on YouTube", command=lambda: open_search(result_label.cget("text").split('\n')[0][2:], "YouTube"), state="disabled")
youtube_button.grid(row=6, column=0, pady=5)

spotify_button = ttk.Button(card_frame, text="Search on Spotify", command=lambda: open_search(result_label.cget("text").split('\n')[0][2:], "Spotify"), state="disabled")
spotify_button.grid(row=6, column=1, pady=5)

apple_music_button = ttk.Button(card_frame, text="Search on Apple Music", command=lambda: open_search(result_label.cget("text").split('\n')[0][2:], "Apple Music"), state="disabled")
apple_music_button.grid(row=7, column=0, columnspan=2, pady=5)

# Save Button
save_button = ttk.Button(card_frame, text="Save Recommendations", command=save_recommendations, state="disabled")
save_button.grid(row=8, column=0, columnspan=2, pady=5)

# Run the Tkinter app
root.mainloop()
