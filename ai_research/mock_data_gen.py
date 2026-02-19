import pandas as pd
import sys
import os

# Allow importing from backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from app.services.recommender import train_recommendation_model

# Create some fake interactions
data = {
    'user_id': [1, 1, 2, 2, 3, 3, 4, 1],
    'product_id': [10, 11, 10, 12, 11, 13, 10, 13],
    'rating': [5, 4, 5, 2, 4, 5, 4, 5]
}

df = pd.DataFrame(data)
train_recommendation_model(df)
print("Artifact created in backend/artifacts/recommender.pkl")


      