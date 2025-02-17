import pandas as pd

# Load CSV file into a DataFrame
file_path = "spotify_millsongdata.csv"  
df = pd.read_csv(file_path)

# Check rows where Spotify link is missing
print("Rows with missing Spotify links:")
print(df[df['spotify_link'].isnull()])

# Remove rows where Spotify link is missing or empty
df_cleaned = df.dropna(subset=['spotify_link'])  
df_cleaned = df_cleaned[df_cleaned['spotify_link'].str.strip() != ""]  

# Save the cleaned DataFrame back to a CSV file
output_file = "cleaned_file.csv"
df_cleaned.to_csv(output_file, index=False)

print(f"Cleaned file saved as {output_file}.")
