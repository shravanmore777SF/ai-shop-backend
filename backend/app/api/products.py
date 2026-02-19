from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sentence_transformers import SentenceTransformer
from ..database import SessionLocal
from ..models import models

router = APIRouter()

# Initialize the AI model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/search")
def search_products(q: str = Query(...), db: Session = Depends(get_db)):
    # 1. Convert search text to vector
    query_vector = model.encode(q).tolist()
    
    # 2. Get the products from the database
    results = db.query(models.Product).order_by(
        models.Product.description_vector.cosine_distance(query_vector)
    ).limit(8).all()
    
    # 3. SAFE SERIALIZATION:
    # We manually pick the fields we want to send to the frontend.
    # This excludes the heavy 'vectors' which cause the 500 Error.
    safe_results = []
    for p in results:
        safe_results.append({
            "id": p.id,
            "name": p.name,
            "category": p.category,
            "price": p.price,
            "rating": p.rating,
            "image_url": p.image_url,
            "product_link": p.product_link
        })
    
    return safe_results

@router.get("/similar/{product_id}")
def get_visually_similar(product_id: int, db: Session = Depends(get_db)):
    target = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not target:
        return {"error": "Product not found"}
    
    # Similar logic for visual similarity
    similar = db.query(models.Product).filter(models.Product.id != product_id).order_by(
        models.Product.image_vector.cosine_distance(target.image_vector)
    ).limit(4).all()

    return [{
        "id": p.id,
        "name": p.name,
        "price": p.price,
        "image_url": p.image_url
    } for p in similar]