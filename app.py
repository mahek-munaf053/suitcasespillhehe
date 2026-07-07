mport streamlit as st
from ai_engine import get_stylist_response

# 1. Page Configuration
st.set_page_config(page_title="SuitcaseSpill 🧳", page_icon="💅🏼", layout="wide")

# 2. Premium Pink Pastel Full-Screen UI Style Injector
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    html, body, [class*="st-"], [class*="css-"], p, span, li, ul, ol, div, button, input {
        font-family: 'Fredoka', sans-serif !important;
    }

    /* Full screen infinite polka-dot background override */
    div[data-testid="stAppViewContainer"] {
        background-color: #ffffff !important;
        background-image: radial-gradient(#FFC0CB 20%, transparent 20%),
                          radial-gradient(#FFC0CB 20%, transparent 20%) !important;
        background-size: 40px 40px !important;
        background-position: 0 0, 20px 20px !important;
    }
    
    div[data-testid="stMainBlockContainer"], header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* Solid Pastel Pink Chat Message Containers */
    [data-testid="stChatMessage"] {
        background-color: #FFC0CB !important;  
        border-radius: 18px !important;
        padding: 18px !important;
        margin-bottom: 12px !important;
        border: none !important;
    }

    /* Force chat avatar picture circles to align cleanly */
    [data-testid="stChatMessageAvatar"] img {
        border-radius: 50% !important;
        border: 2px solid #FFF !important;
        background-color: #FFF !important;
    }

    /* Chat bubble text styling rules */
    [data-testid="stChatMessage"] p, 
    [data-testid="stChatMessage"] span, 
    [data-testid="stChatMessage"] li {
        color: #FFFFFF !important;
        font-size: 17px !important;
    }
    
    /* Targets the text input parent container to handle positioning */
    div.stTextInput {
        position: relative !important;
    }
    
    /* THE ULTIMATE INLINE BOX OVERRIDE */
    div.stTextInput > div > div > input {
        background-color: #FFC0CB !important;
        color: #FFFFFF !important;
        border: 2px solid #FFFFFF !important;
        border-radius: 25px !important;
        padding: 12px 20px !important;
        font-size: 16px !important;
        box-shadow: 0 4px 12px rgba(255, 192, 203, 0.2) !important;
    }
    
    /* Disables all focus states and border line boxes completely */
    div.stTextInput > div, div.stTextInput > div > div {
        border: none !important;
        background-color: transparent !important;
        box-shadow: none !important;
    }

    div.stTextInput input::placeholder {
        color: rgba(255, 255, 255, 0.8) !important;
    }

    div.stTextInput label {
        display: none !important;
    }

    /* Styles the container holding our native sticker placement */
    .sticker-wrapper {
        position: absolute;
        top: -65px; /* Pulls it right over the top of the chat input */
        right: 20px;
        z-index: 999;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Branding Headers (Wrapped inside matching pink block container)
st.markdown("""
    <div style='
        background-color: #FFC0CB; 
        border-radius: 18px; 
        padding: 20px; 
        margin-bottom: 25px; 
        text-align: center;
    '>
        <h1 style='color: #FFFFFF !important; margin: 0; font-size: 42px;'>SuitcaseSpill♡</h1>
        <p style='color: #FFFFFF !important; margin: 5px 0 0 0; font-size: 16px; opacity: 0.95;'>your ai personal travel stylist ꒰ᐢ. .ᐢ꒱</p>
    </div>
""", unsafe_allow_html=True)

# 4. Initialize Onboarding State Variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "step" not in st.session_state:
    st.session_state.step = "ask_destination"
if "trip_data" not in st.session_state:
    st.session_state.trip_data = {
        "destination": "",
        "dates": "",
        "other_cities": "",
        "activities": ""
    }

STYLIST_AVATAR = "bot_avatar.png"
USER_AVATAR = "user_avatar.png"

# Send initial greeting message from the bot if empty
if st.session_state.step == "ask_destination" and len(st.session_state.chat_history) == 0:
    msg = "heyyyy! heading somewhere? 🤭 tell me your main destination city first! 🫶🏼"
    st.session_state.chat_history.append({"role": "assistant", "content": msg})

# Render conversation timeline items
for message in st.session_state.chat_history:
    avatar = USER_AVATAR if message["role"] == "user" else STYLIST_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])

# 5. NO-BUTTON INLINE ENTER TRIGGERS: Clean, standalone text input field!
def handle_chat_input():
    user_reply = st.session_state.user_typed_message
    if user_reply:
        st.session_state.chat_history.append({"role": "user", "content": user_reply})
        
        if st.session_state.step == "ask_destination":
            st.session_state.trip_data["destination"] = user_reply
            bot_msg = "ooh love that place! 😍 what are the dates or how many days are you staying? 📅"
            st.session_state.chat_history.append({"role": "assistant", "content": bot_msg})
            st.session_state.step = "ask_dates"
            
        elif st.session_state.step == "ask_dates":
            st.session_state.trip_data["dates"] = user_reply
            bot_msg = "got it! 📝 will you be traveling to any other cities during this trip? (yes/no - list them if yes!) ✈️"
            st.session_state.chat_history.append({"role": "assistant", "content": bot_msg})
            st.session_state.step = "ask_cities"
            
        elif st.session_state.step == "ask_cities":
            st.session_state.trip_data["other_cities"] = user_reply
            bot_msg = "perfect! now spill the vibes... 💅🏼 what activities do you have planned? (beach clubs, hiking, fancy dinners?)"
            st.session_state.chat_history.append({"role": "assistant", "content": bot_msg})
            st.session_state.step = "ask_activities"
            
        elif st.session_state.step == "ask_activities":
            st.session_state.trip_data["activities"] = user_reply
            
            formatted_input = (
                f"Main Destination city: {st.session_state.trip_data['destination']}\n"
                f"Trip Dates/Duration: {st.session_state.trip_data['dates']}\n"
                f"Other adjacent cities visiting on trip: {st.session_state.trip_data['other_cities']}\n"
                f"Planned Vibes & Activities: {st.session_state.trip_data['activities']}"
            )
            
            payload_history = st.session_state.chat_history[:-1] + [{"role": "user", "content": formatted_input}]
            
            with st.spinner("Styling your lookbook... ✨"):
                ai_reply = get_stylist_response(payload_history)
                st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
                
            st.session_state.step = "completed"
            
        elif st.session_state.step == "completed":
            with st.spinner("Thinking... ✨"):
                ai_reply = get_stylist_response(st.session_state.chat_history)
                st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})

# Create a layout container anchor to lock the sticker to the input component
st.markdown('<div style="position: relative;">', unsafe_allow_html=True)

# Injects the cute transparent animated bunny sticker right above the pink box
st.markdown('<div style="position: relative;">', unsafe_allow_html=True)
st.markdown("""
    <div class="sticker-wrapper">
        <img src="https://imgur.com" width="70">
    </div>
""", unsafe_allow_html=True)

# Main input text bar element
user_reply = st.text_input(
    label="spill_input",
    placeholder="Spill your trip details here...",
    key="user_typed_message",
    on_change=handle_chat_input
)

st.markdown('</div>', unsafe_allow_html=True)

# Block autocomplete dropdowns safely
st.components.v1.html("""
    <script>
    var input = window.parent.document.querySelector('input[type="text"]');
    if (input) {
        input.setAttribute('autocomplete', 'off');
    }
    </script>
""", height=0)
