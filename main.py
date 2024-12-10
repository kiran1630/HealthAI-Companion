from bot import MedicalAssistanceBot
import streamlit as st
import streamlit as st

def home_page():
    st.title("Medical Assistance Chatbot")
    st.write("Ask any health-related questions, and the bot will assist you.")

    # Initialize bot and session state
    if "bot" not in st.session_state:
        st.session_state.bot = MedicalAssistanceBot(session_id="medical_session_001")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []  # Store chat messages as a list of dictionaries

    # Display chat messages using Streamlit chat message
    st.subheader("Chat")
    for chat in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(chat['user'])  # Display user message
        with st.chat_message("assistant"):
            st.write(chat['bot'])  # Display bot response

    # User input using st.chat_input()
    user_input = st.chat_input("Type your question here...")

    # Generate bot response when user submits a message
    if user_input:
        # Append user message to chat history
        st.session_state.chat_history.append({"user": user_input, "bot": None})
        with st.chat_message("user"):
            st.write(user_input)

        # Generate bot response
        bot_response = st.session_state.bot.provide_assistance(
            session_id="medical_session_001",
            input_message=user_input
        )

        # Append bot response to chat history
        st.session_state.chat_history[-1]["bot"] = bot_response
        with st.chat_message("assistant"):
            st.write(bot_response)


def about_page():
  
    # Add a title with an icon
    st.title("🤖 About the Medical Assistance Chatbot")

    # Add a brief description with markdown and emoji
    st.markdown("""
    ### 🌟 What is this chatbot?  
    This AI-powered Medical Assistance Chatbot is designed to help users with general health-related queries. It leverages **state-of-the-art AI models** like **Llama** and **Gemini** to provide concise, informative responses.  

    ### ⚠️ Important Disclaimer:  
    - This chatbot is **not a substitute for professional medical advice**.  
    - Always consult a licensed healthcare professional for accurate diagnosis and treatment.  

    ### 🛠️ Key Features:  
    - 💬 **Interactive Conversations**: Get instant responses to your health-related questions.  
    - 🧠 **Advanced AI Models**: Backed by cutting-edge technology for accuracy.  
    - 🕒 **24/7 Availability**: Your virtual assistant is always ready to help.  

    ---
    """, unsafe_allow_html=True)

    # Add an info message
    st.info("This chatbot is for educational purposes only and should not be used for emergency or critical medical situations.", icon="ℹ️")

   
    # Add buttons for user interaction (e.g., learn more or provide feedback)
    if st.button("💡 Learn More"):
        st.markdown("Visit our [documentation](https://example.com) for detailed information on how the chatbot works!")
    if st.button("✍️ Provide Feedback"):
        st.markdown("We value your feedback! Please share your thoughts [here](https://example.com/feedback).")


def display_all_sessions(bot):
    st.title("📜 Previous Chat Sessions")
    st.write("Below is a list of all chat sessions. Click to expand and view the details.")

    # Fetch all session IDs from the bot's store
    session_ids = list(bot.store.keys())

    if session_ids:
        for session_id in session_ids:
            # Expander for each session
            with st.expander(f"Session: {session_id}"):
                # Retrieve chat logs for the session
                chat_logs = bot.store[session_id].messages  # Assuming 'messages' stores the history

                if chat_logs:
                    for msg in chat_logs:
                        if msg.type == "human":
                            st.markdown(f"**You:** {msg.content}")
                        elif msg.type == "ai":
                            st.markdown(f"**Bot:** {msg.content}")
                else:
                    st.info("This session has no messages.", icon="ℹ️")
    else:
        st.info("No previous chat sessions available.", icon="ℹ️")

# Sidebar Navigation
# st.sidebar.title("Navigation")
# page = st.sidebar.radio("Go to", ["Home", "About", "Previous Chat Sessions"])

# # Display the selected page
# if page == "Home":
#     home_page()
# elif page == "About":
#     about_page()
# elif page == "Previous Chat Sessions":
#    if "bot" not in st.session_state:
#         st.session_state.bot = MedicalAssistanceBot(session_id="default_session")
#    display_all_sessions(st.session_state.bot)

def app():
    # Set the page configuration
    st.set_page_config(page_title="Medical Assistance Chatbot", page_icon="🩺", layout="wide")

    # Sidebar Navigation
    with st.sidebar:
        st.title("🔍 Navigation")
        page = st.selectbox("Choose a section", ["Home", "About", "Previous Chat Sessions"])

        # Add a custom sidebar image or text
        #st.image("https://via.placeholder.com/150", caption="Your Medical Assistant", use_column_width=True)
        st.markdown("Powered by **Llama-3.1** and **Gemini**")
        st.markdown("---")
        st.write("📞 Support: medbot108@gmail.com")

    # Initialize bot and session state
    if "bot" not in st.session_state:
        st.session_state.bot = MedicalAssistanceBot(session_id="default_session")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Page Logic
    if page == "Home":
        home_page()
    elif page == "About":
        about_page()
    elif page == "Previous Chat Sessions":
        display_all_sessions(st.session_state.bot)

if __name__ == "__main__":
    app()