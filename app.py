import streamlit as st 
import json 
import openai
import os
from dotenv import load_dotenv
from googletrans import Translator

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

translator = Translator()

def generate_questions(tech_stack):
    prompt = f"Generate 3-5 technical questions to asses proficiency in the following technologies: {tech_stack}"
    try:
        response = openai.Completion.create(
            engine = "text-davinci-003",
            prompt=prompt,
            max_tokens=300,
        )
        return response.chouces[0].text.strip()
    except Exception as e:
        return f"Error generating questions: {e}"
    

def analyze_sentiment(text):
    prompt = f"Analyze the sentiment of the following text: {text}. Return one of the : Positive, Neutral, Negative."
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt = prompt,
            max_tokens = 10,
            
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error analyzing sentiment: {e}"

def save_candidate_data(candidate_data):
    with open("candidate_data.json", "a") as f:
        json.dump(candidate_data, f)
        f.write("\n")
        
def fetch_candidate_data(email):
    try:
        with open("candidate_data.json", "r") as f:
            for line in f:
                data = json.loads(line)
                if data.get["email"] == email:
                    return data
    except FileNotFoundError:
        return None
    return None

def translate_text(text, target_language):
    try:
        return translator.translate(text, dest=target_language).text
    except Exception as e:
        return f"Error translating text: {e}"

def greet_user(language="en"):
    greeting = "Hello! Welcome to the TalentScout Hiring Assistant. I am here tohelp you with the initial screeing process."
    if language!="en":
        greeting = translate_text(greeting, language)
    st.write(greeting)
    

def end_conversation(language="en"):
    text = "Thank you for using TalentScout! We will review the information you provided and get back to you shortly."
    if language != "en":
        text = translate_text(text, language)
    st.write(text)
    st.stop()

st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={"About":"This is the talentScout HiriNG Assistant."},
    
)

st.sidebar.header("Settings")
language = st.sidebar.selectbox("Select Language", ["English","Hindi","Spanish", "French"])

greet_user(language)

st.header("Candidate Information")
name= st.text_input("Full Name")
email = st.text_input("Email Id")
phone = st.text_input("Phone Number")
experience = st.number_input("Years of Experience", min_value=0, max_value=50, step=1)
position = st.text_input("Position Applied For")
location = st.text_input("Current Location")

st.header("Technical Skills")
tech_stack = st.text_input(
    "Specify the technologies you are proficient in, separated by commas", 
    placeholder = "Programming Languages, Frameworks, Tools, etc."
)

conversation_history = []

