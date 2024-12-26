# 5-Star Hotel Chatbot

This project is a chatbot designed for a 5-star hotel concierge, providing users with assistance for room service orders, special requests, hotel amenities information, and general inquiries. It uses natural language processing (NLP) techniques for intent recognition and matching, ensuring a seamless guest experience.

## Features

- **Interactive Chat Interface**: Users can chat with the chatbot and receive responses to various hotel-related inquiries.
- **Conversation History**: The chatbot keeps a log of all conversations, making it easy to track past interactions.
- **Suggestion System**: The chatbot offers suggestions to help users with common questions.
- **Room Service & Hotel Inquiries**: Guests can inquire about services, amenities, and make requests via the chatbot.

## Installation

### Prerequisites

Make sure you have the following installed:

- Python 3.x
- Streamlit
- NLTK
- Other dependencies can be installed using the requirements file.

### Steps to Run the Chatbot

1. Clone this repository:

    ```bash
    git clone https://github.com/yourusername/5-star-hotel-chatbot.git
    cd 5-star-hotel-chatbot
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the chatbot app using Streamlit:

    ```bash
    streamlit run app.py
    ```

4. Visit the local URL provided by Streamlit to interact with the chatbot.

## File Structure

- `app.py`: The main application that runs the chatbot using Streamlit.
- `newintents.json`: The file containing intents and patterns for chatbot responses.
- `chat_log.csv`: The log of all conversations between users and the chatbot.
- `requirements.txt`: Contains all the Python dependencies needed for the project.

## How It Works

The chatbot uses Natural Language Processing (NLP) and pattern matching techniques to understand user inputs and generate appropriate responses. The key features include:

1. **Intent Matching**: The chatbot matches user inputs to predefined patterns and selects the best response based on a similarity score.
2. **Suggestions**: The chatbot provides suggestions based on common user queries to improve interaction.
3. **Chat Log**: Conversations are logged in a CSV file for review and analysis.

## About the 5-Star Hotel Chatbot

The 5-Star Hotel Chatbot serves as a virtual concierge, enabling guests to interact with hotel services through a conversational interface. The chatbot is designed to handle a wide range of tasks, including:

- **Room Service Orders**: The chatbot can help guests place orders for food and beverages.
- **Special Requests**: Guests can make special requests, such as extra pillows, room cleaning, or other amenities.
- **Hotel Amenities**: Information about the hotel's amenities, including the gym, pool, spa, and dining options, can be accessed via the chatbot.
- **General Inquiries**: The chatbot answers general questions about the hotel's policies, check-in/check-out times, directions, and more.

Built with NLP and enhanced pattern matching, this chatbot ensures a seamless guest experience by providing quick, accurate, and friendly responses.

## Contributions

Feel free to contribute by reporting issues, submitting pull requests, or suggesting improvements!
