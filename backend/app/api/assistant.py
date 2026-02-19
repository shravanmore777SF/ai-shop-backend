from groq import Groq
from fastapi import APIRouter, Query, HTTPException
import os
from dotenv import load_dotenv

router = APIRouter()

# --- STEP 1: Paste your Groq API Key here ---
load_dotenv() # This loads variables from your .env file
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

@router.get("/chat")
def chat_with_assistant(user_query: str = Query(...), context_products: str = Query(...)):
    try:
        # STEP 2: Using the Llama 3 model (very reliable and free)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a helpful Indian e-commerce assistant. Provide a 2-sentence recommendation based on the provided products."
                },
                {
                    "role": "user", 
                    "content": f"I am looking for: {user_query}. In my shop, I found these: {context_products}. Explain why these are good."
                }
            ],
            temperature=0.7,
            max_tokens=100
        )
        
        return {"assistant_response": completion.choices[0].message.content}

    except Exception as e:
        # STEP 3: Check your VS Code terminal for this print!
        print(f"FATAL GROQ ERROR: {e}")
        return {"assistant_response": "Our AI assistant is currently updating its catalog. Here are the best matches from our shop!"}