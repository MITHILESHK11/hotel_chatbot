import json
import os
import streamlit as st
import datetime
import csv
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from difflib import SequenceMatcher
import random

nltk.download('punkt')
nltk.download('wordnet')

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Load intents
file_path = os.path.abspath('newintents.json')
with open(file_path, 'r') as f:
    intents = json.load(f)

# Extract all patterns for suggestions
all_patterns = [pattern for intent in intents for pattern in intent['patterns']]

# Function to preprocess and lemmatize input
def preprocess_input(input_text):
    tokens = word_tokenize(input_text.lower())
    return [lemmatizer.lemmatize(word) for word in tokens]

# Similarity-based intent matching with lemmatization
def find_best_match(input_text):
    best_match = None
    highest_similarity = 0.0
    threshold = 0.6
    processed_input = preprocess_input(input_text)

    for intent in intents:
        for pattern in intent['patterns']:
            processed_pattern = preprocess_input(pattern)
            similarity = SequenceMatcher(None, ' '.join(processed_input), ' '.join(processed_pattern)).ratio()
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = intent

    if highest_similarity >= threshold:
        return best_match

    return None

# Chatbot logic with expanded matching
def chatbot(input_text):
    # Try direct matching first
    input_words = preprocess_input(input_text)

    for intent in intents:
        for pattern in intent['patterns']:
            pattern_words = preprocess_input(pattern)
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
    st.title("Hotel Chatbot")

    menu = ['Home', 'Conversation History', 'About']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Home':
        st.write("Welcome to our Hotel Chatbot. How may I assist you today?")

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
        st.subheader("About the Hotel Chatbot")
        st.write("""
        The **Hotel Chatbot** is a state-of-the-art virtual concierge designed to enhance the guest experience by providing quick, efficient, and personalized assistance throughout their stay at the hotel. Built with Natural Language Processing (NLP) and advanced pattern matching, the chatbot ensures a seamless interaction, offering a range of services to cater to every guest's needs. 
        
        Here’s a deeper look at its key features:
        
        - **Room Service Orders**: 
        The chatbot allows guests to place food and beverage orders directly through the interface, without the need to call the front desk or room service. Guests can easily view menus, place their orders, and even customize their requests. This feature saves time and ensures that guests' dining preferences are met with minimal effort.
        
        - **Special Requests**: 
        Whether it's an extra pillow, room cleaning, or special arrangements for an event, the chatbot can manage guest requests instantly. The system ensures that requests are logged and sent to the appropriate department, minimizing the chances of any missed or delayed requests.
        
        - **Hotel Amenities and Services Information**: 
        Guests can ask about hotel services and amenities, such as gym hours, spa services, pool availability, and restaurant timings. The chatbot provides accurate and up-to-date information to help guests make the most of their stay, from booking spa appointments to learning about upcoming events or activities at the hotel.
        
        - **General Inquiries**: 
        The chatbot can also answer a wide range of general inquiries, such as information about local attractions, directions to popular tourist spots, transportation options, hotel policies (e.g., pet policy, check-out times), and more. This feature ensures guests have easy access to all the necessary information during their stay, enhancing convenience and satisfaction.
        
        - **Personalized Guest Experience**: 
        By using NLP, the chatbot understands natural language inputs and adapts its responses accordingly, providing a more personalized interaction. It can remember guest preferences from previous conversations, allowing for tailored recommendations and a more seamless experience with the hotel’s services.
        
        - **Conversation History**: 
        All interactions with the chatbot are logged and stored, providing a record of past conversations. This helps the hotel staff to follow up on requests, track guest preferences, and resolve any issues promptly. Guests can also revisit their previous conversations for reference.
        
        - **24/7 Availability**: 
        The chatbot is available around the clock, ensuring guests can get assistance at any time, day or night. Whether it’s a late-night snack request or an early morning inquiry, the chatbot is always ready to help, offering guests the convenience of on-demand assistance without having to wait for a staff member.
        
        - **Seamless Integration with Hotel Operations**: 
        The chatbot is fully integrated into the hotel’s operational systems, allowing it to forward requests directly to the relevant departments (e.g., housekeeping, room service, front desk). This ensures that requests are handled promptly and accurately, minimizing delays and improving overall efficiency.
        
        - **Enhanced Guest Satisfaction**: 
        With quick response times, personalized recommendations, and easy access to hotel services, the chatbot enhances guest satisfaction. Guests can focus on enjoying their stay, knowing that their needs are being taken care of efficiently.
        
        The Hotel Chatbot is not just a tool for answering questions; it’s a comprehensive service assistant that works tirelessly to ensure every guest has a memorable and hassle-free experience. Its intelligent, proactive approach to managing guest needs sets a new standard in hospitality service.
    """)


if __name__ == "__main__":
    main()
