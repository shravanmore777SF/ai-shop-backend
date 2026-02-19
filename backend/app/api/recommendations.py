from fastapi import APIRouter, HTTPException
from ..services.recommender import get_user_recs

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.get("/{user_id}")
async def read_recommendations(user_id: int):
    """
    Fetches personalized product recommendations for a specific user 
    using the trained similarity matrix.
    """
    recs = get_user_recs(user_id)
    if not recs:
        # Fallback if no specific recommendations are found
        return {"user_id": user_id, "recommendations": [], "status": "No history found for user"}
    
    return {"user_id": user_id, "recommended_product_ids": recs}