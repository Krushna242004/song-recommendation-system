import pandas as pd
import pickle

try:
    music = pd.read_csv('cleaned_file.csv')
    
    # Ensure the required columns are present
    if not {'artist', 'song', 'spotify_link'}.issubset(music.columns):
        raise ValueError("Missing required columns in the dataset. Ensure 'artist', 'song', and 'spotify_link' are present.")

    # Drop rows with missing values in essential columns
    music.dropna(subset=['artist', 'song', 'spotify_link'], inplace=True)

    # Select only relevant columns
    music_data = music[['artist', 'song', 'spotify_link']]

    # Save the DataFrame as a pickle file
    with open('df.pkl', 'wb') as file:
        pickle.dump(music_data, file)
    
    print("df.pkl created successfully!")
except Exception as e:
    print(f"Error: {e}")
