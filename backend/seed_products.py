import pandas as pd
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import models

def seed_amazon_data():
    db = SessionLocal()
    # Read only the first 500 items to keep it manageable
    df = pd.read_csv("amazon.csv").head(500)
    
    for _, row in df.iterrows():
        product = models.Product(
            name=row['product_name'],
            category=row['category'],
            price=row['discounted_price'],
            rating=row['rating'],
            image_url=row['img_link'],
            product_link=row['product_link']
        )
        db.add(product)
    db.commit()
    print("✅ 500 Amazon products seeded!")

if __name__ == "__main__":
    seed_amazon_data()