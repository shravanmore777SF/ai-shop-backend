import json
import os
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import models

def seed_database():
    db = SessionLocal()
    
    # This logic finds the folder where THIS script is saved
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # This points to the json file in that same folder
    json_path = os.path.join(script_dir, "amazon_vectors.json")

    print(f"Checking for file at: {json_path}")

    if not os.path.exists(json_path):
        print(f"❌ ERROR: File not found at {json_path}")
        print("Make sure 'amazon_vectors.json' is in the 'backend' folder.")
        return

    with open(json_path, "r") as f:
        data = json.load(f)

    print(f"🚀 Found {len(data)} items. Starting database injection...")

    # Optional: Clear existing products to prevent duplicates
    db.query(models.Product).delete()

    for item in data:
        product = models.Product(
            name=item['name'],
            category=item['category'],
            price=item['price'],
            rating=item['rating'],
            image_url=item['image_url'],
            product_link=item['product_link'],
            description_vector=item['description_vector'],
            image_vector=item['image_vector']
        )
        db.add(product)
    
    db.commit()
    db.close()
    print("✅ Success! Database is now populated with Amazon products and AI vectors.")

if __name__ == "__main__":
    seed_database()