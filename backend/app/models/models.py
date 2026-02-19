from sqlalchemy import Column, Integer, String, Float
from pgvector.sqlalchemy import Vector
from ..database import Base

class User(Base):
    """
    User model for authentication and profiles.
    """
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Product(Base):
    """
    Product model optimized for the Amazon Sales Dataset and AI Vector Search.
    """
    __tablename__ = "products"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String)
    
    # Prices in the Amazon dataset often contain currency symbols (e.g., ₹), 
    # so we store them as Strings and convert to Float during calculations if needed.
    price = Column(String) 
    
    # Store average customer ratings
    rating = Column(Float)
    
    # Links to the Amazon images and product pages
    image_url = Column(String)
    product_link = Column(String)
    
    # --- AI Vector Columns ---
    # description_vector (384-dim) matches 'all-MiniLM-L6-v2' used in Colab
    description_vector = Column(Vector(384))
    
    # image_vector (512-dim) matches 'clip-ViT-B-32' used in Colab
    image_vector = Column(Vector(512))