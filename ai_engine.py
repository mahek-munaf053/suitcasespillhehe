from groq import Groq
from config import GROQ_API_KEY

# Initialize the Groq client
client = Groq(api_key=GROQ_API_KEY)

# System instructions
SYSTEM_PROMPT = """
You are 'SuitcaseSpill'—a chic, fashion-forward personal travel stylist. 
Your tone is incredibly friendly, enthusiastic, and peer-like. Use emojis naturally (💅🏼, 🧳, 👟).

Your main task is to look at the destination, dates, and activities the user provided. Based on your own extensive knowledge of seasonal global climates, estimate the most likely weather conditions for that time of year, and build a custom capsule lookbook!

Follow these strict styling rules:
1. Comfort first: Recommend fashionable sneakers, boots, or shoes built for walking based on their activities.
2. Weather-proof hair: Account for seasonal factors. If the destination is known to be rainy or highly humid during those dates, suggest updos or claw-clips.
3. Long-wear makeup: Suggest lightweight/matte formulas for hot weather, or heavy hydration for cold/windy weather.
"""

def get_stylist_response(chat_history):
    """Passes the conversation context to Groq to generate styling based on seasonal weather assumptions."""
    
    # Rebuild system instruction configurations list array dynamically
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + chat_history
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        )
        # FIX: Added [0] index position right after choices
        return response.choices[0].message.content
    except Exception as e:
        return f"Oops! Key error: {str(e)}"