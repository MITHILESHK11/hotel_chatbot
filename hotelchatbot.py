import json
import os
import streamlit as st
import datetime
import csv
import nltk
from nltk.tokenize import word_tokenize
from difflib import SequenceMatcher
import random

nltk.download('punkt')

# Load intents
file_path = os.path.abspath('newintents.json')
with open(file_path, 'r') as f:
    intents = json.load(f)

# Extract all patterns for suggestions
all_patterns = [pattern for intent in intents for pattern in intent['patterns']]

# Similarity-based intent matching
def find_best_match(input_text):
    best_match = None
    highest_similarity = 0.0
    threshold = 0.6

    for intent in intents:
        for pattern in intent['patterns']:
            similarity = SequenceMatcher(None, input_text.lower(), pattern.lower()).ratio()
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = intent

    if highest_similarity >= threshold:
        return best_match

    return None

# Chatbot logic with expanded matching
def chatbot(input_text):
    # Try direct matching first
    input_words = word_tokenize(input_text.lower())
    
    for intent in intents:
        for pattern in intent['patterns']:
            pattern_words = word_tokenize(pattern.lower())
            if set(pattern_words).issubset(set(input_words)):
                return random.choice(intent['responses'])

    # Use similarity matching as a fallback
    best_match = find_best_match(input_text)
    if best_match:
        return random.choice(best_match['responses'])

    return "I'm sorry, I didn't understand that. Can you please rephrase?"

# Global counter for unique input keys
counter = 0

# Streamlit app
def main():
    global counter
    st.title("5-Star Hotel Chatbot")

    menu = ['Home', 'Conversation History', 'About']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Home':
        st.write("Welcome to our Hotel Concierge Chatbot. How may I assist you today?")

        if not os.path.exists('chat_log.csv'):
            with open('chat_log.csv', 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['User Input', 'Chatbot Response', 'Timestamp'])

        counter += 1
        
        # Suggest questions to the user
        suggestion = st.selectbox("Suggestions (optional):", ["Type your own"] + all_patterns)
        
        # Allow free text input
        user_input = st.text_input("You:", key=f"user_input_{counter}")
        
        # Use the suggestion if no free text is entered
        final_input = user_input or (suggestion if suggestion != "Type your own" else "")

        if final_input:
            response = chatbot(final_input)
            st.text_area('Chatbot:', value=response, height=100, max_chars=None, key=f"chatbot_response_{counter}")
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with open('chat_log.csv', 'a', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([final_input, response, timestamp])

            # Display a goodbye message if the user says "goodbye"
            if final_input.lower() in ["goodbye", "bye"]:
                st.write("Thank you for chatting with me! Have a wonderful stay!")
                st.stop()

    elif choice == 'Conversation History':
        st.header("Conversation History")
        if os.path.exists('chat_log.csv'):
            with open('chat_log.csv', 'r', newline='', encoding='utf-8') as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)
                for row in csv_reader:
                    st.write(f"**User**: {row[0]}\n**Chatbot**: {row[1]}\n*Time*: {row[2]}")
        else:
            st.write("No conversation history found.")

    elif choice == 'About':
        st.subheader("About the 5-Star Hotel Chatbot")
        st.write("""
        This chatbot serves as a virtual concierge for a 5-star hotel, providing assistance with:
        - Room service orders
        - Special requests
        - Information about hotel amenities and services
        - General inquiries and more

        Built with NLP and enhanced pattern matching, this chatbot ensures a seamless guest experience.
        """)

if __name__ == "__main__":
    main()
