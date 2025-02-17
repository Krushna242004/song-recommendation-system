#it's just focused on loading and checking the similarity matrix
import pickle

# Similarity matrix ko pickle se load karo
with open('similarity.pkl', 'rb') as file:
    similarity = pickle.load(file)

# Matrix ki shape check karo
print("Loaded similarity matrix shape:", similarity.shape)

# Matrix ka ek part print karo (optional)
print("\nPart of the similarity matrix:")
print(similarity[:5, :5].toarray())  # Pehla 5x5 block dense format me dekho
