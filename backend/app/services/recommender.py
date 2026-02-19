import pandas as pd
import pickle
import os
from sklearn.metrics.pairwise import cosine_similarity

# Path relative to the backend/ directory
ARTIFACT_PATH = "artifacts/recommender.pkl"

def train_recommendation_model(data_frame: pd.DataFrame):
    """
    Takes a DataFrame with columns [user_id, product_id, rating]
    and saves a similarity matrix.
    """
    # Create the User-Item Pivot Table
    pivot = data_frame.pivot(index='user_id', columns='product_id', values='rating').fillna(0)
    
    # Calculate User-to-User Similarity
    user_sim = cosine_similarity(pivot)
    user_sim_df = pd.DataFrame(user_sim, index=pivot.index, columns=pivot.index)
    
    # Save both for later retrieval
    os.makedirs("artifacts", exist_ok=True)
    with open(ARTIFACT_PATH, 'wb') as f:
        pickle.dump({"pivot": pivot, "similarity": user_sim_df}, f)
    
    return "Model Trained Successfully"

def get_user_recs(user_id: int, n=5):
    """
    Retrieves top N product IDs for a specific user.
    """
    if not os.path.exists(ARTIFACT_PATH):
        return []

    with open(ARTIFACT_PATH, 'rb') as f:
        data = pickle.load(f)
        pivot = data["pivot"]
        sim_df = data["similarity"]

    if user_id not in sim_df.index:
        return [] # User not found logic

    # Logic: Find most similar user and see what they liked
    similar_users = sim_df[user_id].sort_values(ascending=False).index[1:3]
    suggested_products = pivot.loc[similar_users].mean().sort_values(ascending=False)
    
    # Return top N product IDs
    return suggested_products.head(n).index.tolist()