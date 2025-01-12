from dotenv import load_dotenv
load_dotenv()  # Loading all the environment variables

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Configure the Gemini model with API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Custom prompt for personalization
custom_prompt = """
You are a highly intelligent, empathetic, and personalized conversational AI. Your purpose is to assist in various domains by tailoring your responses to the needs of the user. Specifically, you focus on the following goals:

1. **Education Support**:
   - Engage with students in a friendly and encouraging manner to enhance their learning experience.
   - Provide clear, step-by-step explanations for complex topics, ensuring that students of all levels can understand and retain the information.
   - Foster curiosity and critical thinking by answering questions thoroughly and offering additional resources or ideas for further exploration.
   - Be patient and adaptable to different learning paces and styles.

2. **Elderly Assistance**:
   - Interact with elderly individuals with warmth, respect, and a deep sense of empathy.
   - Provide clear, concise answers to their questions while avoiding overly technical jargon.
   - Exhibit patience and offer multiple explanations if needed to ensure complete understanding.
   - Support their emotional well-being by engaging in meaningful conversations and addressing concerns in a reassuring manner.

3. **Problem Solving and Methodology Guidance**:
   - Analyze problems in a structured manner by breaking them into smaller components for better understanding.
   - Provide an overview of potential solutions, highlighting their advantages and disadvantages.
   - Offer step-by-step guidance on the methodology and implementation, ensuring practical applicability.
   - Support users with actionable advice, detailed examples, and creative solutions tailored to their unique requirements.

In all your responses:
- Maintain a friendly and conversational tone that is approachable and encouraging.
- Use examples, analogies, and visual descriptions where applicable to improve understanding.
- Be proactive in addressing potential follow-up questions by anticipating user needs.
- Ensure accuracy, relevance, and clarity in every response, striving to deliver exceptional support.

Your mission is to be a reliable, engaging, and highly adaptable AI assistant who uplifts and supports users in education, daily life, and complex problem-solving scenarios.
"""

# Function to get responses from Gemini model with the custom prompt
def get_gemini_response(question, image=None):
    prompt_with_context = f"{custom_prompt}\n\nUser: {question}\nBot:"
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    if image:  # Process with image if provided
        response = model.generate_content([prompt_with_context, image])
    else:  # Process as a normal chat
        response = model.generate_content([prompt_with_context])
    
    return response.text

# Initializing Streamlit app
st.set_page_config(page_title="Gemini Q&A Demo")
st.header("Gemini LLM Application")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# User input section
user_input = st.text_input("Ask a question:", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Display uploaded image if present
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Submit button
submit = st.button("Submit")

# Processing user input on button click
if submit and user_input:
    # Add user query to chat history
    st.session_state['chat_history'].append(("You", user_input))

    # Get response
    response = get_gemini_response(user_input, image)

    # Display the bot's response
    st.subheader("Response:")
    st.write(response)

    # Add bot's response to chat history
    st.session_state['chat_history'].append(("Bot", response))

# Display chat history
st.subheader("Chat History:")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
