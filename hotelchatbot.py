import os
import json
import random
import nltk
import datetime
import streamlit as st
import sklearn
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from difflib import SequenceMatcher

# Ensure NLTK 'punkt' is downloaded only if not present
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Load intents from JSON file
file_path = os.path.abspath('newintents.json')
with open(file_path, 'r') as f:
    intents = json.load(f)

# Extract all patterns for suggestions
all_patterns = [pattern for intent in intents for pattern in intent['patterns']]

# Vectorize patterns using TF-IDF
def vectorize_patterns(intents):
    patterns = [pattern for intent in intents for pattern in intent['patterns']]
    vectorizer = TfidfVectorizer()
    pattern_vectors = vectorizer.fit_transform(patterns)
    return vectorizer, pattern_vectors

# Similarity-based intent matching with cosine similarity
def find_best_match(input_text, vectorizer, pattern_vectors, threshold=0.6):
    input_vector = vectorizer.transform([input_text.lower()])
    similarity_scores = cosine_similarity(input_vector, pattern_vectors)
    highest_similarity = max(similarity_scores[0])
    
    if highest_similarity >= threshold:
        best_match_idx = similarity_scores[0].argmax()
        best_match = intents[best_match_idx // len(intents[0]['patterns'])]
        return best_match
    return None

# Chatbot logic with TF-IDF and cosine similarity
def chatbot(input_text, vectorizer, pattern_vectors):
    best_match = find_best_match(input_text, vectorizer, pattern_vectors)
    
    if best_match:
        return random.choice(best_match['responses'])

    return "I'm sorry, I didn't understand that. Can you please rephrase?"

# Streamlit app
def main():
    st.set_page_config(page_title="5-Star Hotel Chatbot", page_icon="🏨", layout="wide")
    st.title("5-Star Hotel Chatbot")
    st.image("start5hotel.jpg", width=200)

    if "conversation" not in st.session_state:
        st.session_state["conversation"] = []

    # Vectorize patterns during app startup
    vectorizer, pattern_vectors = vectorize_patterns(intents)

    menu = ['Home', 'Conversation History', 'About']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Home':
        st.write("Welcome to our Hotel Concierge Chatbot. How may I assist you today?")

        suggestion = st.selectbox("Suggestions (optional):", ["Type your own"] + all_patterns)

        user_input = st.text_input("You:")

        final_input = user_input or (suggestion if suggestion != "Type your own" else "")

        if final_input:
            response = chatbot(final_input, vectorizer, pattern_vectors)
            st.text_area('Chatbot:', value=response, height=100, max_chars=None, key="chatbot_response")
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            st.session_state["conversation"].append({
                "user": final_input,
                "bot": response,
                "time": timestamp,
            })

            if final_input.lower() in ["goodbye", "bye"]:
                st.write("Thank you for chatting with me! Have a wonderful stay!")
                st.stop()

    elif choice == 'Conversation History':
        st.header("Conversation History")
        if st.session_state["conversation"]:
            for entry in st.session_state["conversation"]:
                st.write(f"**User**: {entry['user']}\n**Chatbot**: {entry['bot']}\n*Time*: {entry['time']}")
        else:
            st.write("No conversation history found.")

    elif choice == 'About':
        st.subheader("About the 5-Star Hotel Chatbot")
        st.write("""
        Welcome to the 5-Star Hotel Chatbot! This chatbot is designed to act as a virtual concierge for guests at a luxurious hotel. It aims to provide timely, efficient, and accurate assistance to guests, enhancing their experience throughout their stay.

        The chatbot is capable of handling a wide range of inquiries, from room bookings and restaurant reservations to answering general questions about the hotel amenities and services. Whether you're looking to book a spa treatment, inquire about the hotel's history, or get recommendations for nearby attractions, the chatbot is here to help.

        **Core Features:**
        - **Room Booking**: The chatbot can assist in checking room availability, booking reservations, and modifying existing bookings.
        - **Restaurant Reservations**: Guests can make dining reservations, explore restaurant menus, and request recommendations.
        - **Hotel Services**: The chatbot provides information about various hotel services like housekeeping, laundry, room service, and concierge services.
        - **Guest Support**: In case of any special requests or issues, the chatbot can quickly connect guests with the appropriate hotel staff.

        **Technology Stack:**
        - **Natural Language Processing (NLP)**: The chatbot uses NLP techniques to understand and respond to user queries. It leverages a variety of intent matching algorithms to provide accurate and relevant answers.
        - **Machine Learning**: The chatbot's core intelligence is powered by machine learning models that continuously improve its ability to understand and respond to user inputs.
        - **Streamlit**: The user interface is built using Streamlit, allowing for a seamless and interactive chat experience. Streamlit makes it easy to create beautiful and interactive data applications, perfect for our chatbot's use case.

        **How It Works:**
        The chatbot uses a combination of predefined intents and patterns to match user inputs and provide appropriate responses. If a direct match is not found, a similarity-based approach is used to find the closest match. The bot also supports feedback submission, which allows users to send feedback directly to the hotel via email.

        **Why Use the Chatbot?**
        - **24/7 Availability**: The chatbot is available at all times, providing immediate responses to guest queries, ensuring a hassle-free experience.
        - **Efficiency**: By automating many tasks, the chatbot saves time for both guests and hotel staff, allowing for faster service and better resource management.
        - **Personalized Service**: The chatbot tailors its responses to individual guest needs and preferences, making each interaction more personalized.
        
        We hope that you enjoy using the 5-Star Hotel Chatbot, and we are committed to continuously improving it to serve you better. If you have any feedback or suggestions, feel free to let us know!
        """)

if __name__ == "__main__":
    main()
