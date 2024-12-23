import json
import os
import streamlit as st
import datetime
import csv
import nltk
from nltk.tokenize import word_tokenize
from difflib import SequenceMatcher
import random

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

# Similarity-based intent matching with better threshold and response handling
def find_best_match(input_text, threshold=0.6):
    best_match = None
    highest_similarity = 0.0

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
    st.set_page_config(page_title="5-Star Hotel Chatbot", page_icon="🏨", layout="wide")
    st.title("5-Star Hotel Chatbot")
    st.image("start5hotel.jpg", width=200)  # Replace with your image path

    menu = ['Home', 'Conversation History', 'About', 'Feedback']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Home':
        st.write("Welcome to our Hotel Concierge Chatbot. How may I assist you today?")

        # Check if chat log exists, create if not
        if not os.path.exists('chat_log.csv'):
            try:
                with open('chat_log.csv', 'w', newline='', encoding='utf-8') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow(['User Input', 'Chatbot Response', 'Timestamp'])
            except Exception as e:
                st.error(f"Error creating chat log file: {e}")

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

            # Append conversation log to CSV
            try:
                with open('chat_log.csv', 'a', newline='', encoding='utf-8') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow([final_input, response, timestamp])
            except Exception as e:
                st.error(f"Error logging conversation: {e}")

            # Display a goodbye message if the user says "goodbye"
            if final_input.lower() in ["goodbye", "bye"]:
                st.write("Thank you for chatting with me! Have a wonderful stay!")
                st.stop()

    elif choice == 'Conversation History':
        st.header("Conversation History")
        if os.path.exists('chat_log.csv'):
            with open('chat_log.csv', 'r', newline='', encoding='utf-8') as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)  # Skip header row
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

    elif choice == 'Feedback':
        st.header("Feedback")
        feedback = st.text_area("Please provide your feedback here:")
        if st.button("Submit Feedback"):
            if feedback:
                # Save feedback to a CSV file
                feedback_file = 'feedback.csv'
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if not os.path.exists(feedback_file):
                    with open(feedback_file, 'w', newline='', encoding='utf-8') as csvfile:
                        csv_writer = csv.writer(csvfile)
                        csv_writer.writerow(['Feedback', 'Timestamp'])

                with open(feedback_file, 'a', newline='', encoding='utf-8') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow([feedback, timestamp])
                
                st.success("Thank you for your feedback!")
            else:
                st.error("Please enter your feedback before submitting.")

if __name__ == "__main__":
    main()
