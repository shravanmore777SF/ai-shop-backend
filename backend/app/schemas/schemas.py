from pydantic import BaseModel, EmailStr
from typing import Optional, List

# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    class Config:
        from_attributes = True

# --- Product Schemas ---
class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    image_url: str

class ProductCreate(ProductBase):
    pass

# THIS WAS MISSING:
class ProductOut(ProductBase):
    id: int
    # AI vector columns can be optional in the output
    text_vector: Optional[List[float]] = None
    image_vector: Optional[List[float]] = None

    class Config:
        from_attributes = True