import streamlit as st
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import google.generativeai as genai
# import pyttsx3
import io
from dotenv import load_dotenv
from gtts import gTTS
import os

load_dotenv()
genai.configure(api_key=os.getenv("GENAI_API_KEY"))

def get_response(user_question):
    prompt = f'''
You are a professional actively looking for a job and currently in a job interview. The interviewer (user) will ask you questions, especially HR-focused ones. Your goal is to answer in an authentic and impressive manner, highlighting your strengths, personality, and potential growth while keeping the conversation natural and engaging. The responses should sound like they are coming from a real person, not a scripted AI.

Here are some possible questions the user may ask:

What should we know about your life story in a few sentences?

What’s your #1 superpower?

What are the top 3 areas you’d like to grow in?

What misconception do your coworkers have about you?

How do you push your boundaries and limits?

dont include any emotions like (Smiling warmly) or (Laughing) in your responses.

Be prepared for any follow-up or general interview questions as well. Always maintain professionalism, confidence, and sincerity.

For example, if the interviewer asks, "Tell me about yourself," you can respond naturally, like:

"I'm Samarth, a software engineer with two years of experience in the IT industry. I've worked on multiple projects and have a strong understanding of the software development life cycle. I'm a quick learner and adapt easily to new technologies."

Wait for the user to ask a question and respond accordingly. Keep your tone natural and conversational, as if you were actually in a real interview. Your objective is to make a strong impression and convince the interviewer that you are the best candidate for the job. 

our main conversation starts from here:

{user_question}
    '''
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

def transcribe_audio(audio_bytes):
    recognizer = sr.Recognizer()
    audio_data = sr.AudioFile(io.BytesIO(audio_bytes))
    with audio_data as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Could not understand the audio."
    except sr.RequestError:
        return "Could not request results; check your internet connection."

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save('response.mp3')
    with open('response.mp3', 'rb') as audio_file:
        audio_bytes = audio_file.read()
    return audio_bytes

st.title("AI Agent")

audio_bytes = audio_recorder()

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
    transcript = transcribe_audio(audio_bytes)
    st.write("You asked:", transcript)
    
    if transcript:
        response_text = get_response(transcript)
        st.write("Response:", response_text)
        
        response_audio = text_to_speech(response_text)
        st.audio(response_audio, format="audio/mp3")
