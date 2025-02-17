import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import save_npz

# Load dataset
try:
    df = pd.read_csv('cleaned_file.csv')

    # Handle missing 'song' values
    df['song'] = df['song'].fillna('')

    # Vectorize the 'song' column
    cv = CountVectorizer(stop_words='english')
    vectors = cv.fit_transform(df['song'])

    # Compute sparse cosine similarity
    similarity_sparse = cosine_similarity(vectors, dense_output=False)

    # Save the sparse similarity matrix
    save_npz('similarity_sparse.npz', similarity_sparse)
    print("similarity_sparse.npz created successfully!")
except Exception as e:
    print(f"Error: {e}")
