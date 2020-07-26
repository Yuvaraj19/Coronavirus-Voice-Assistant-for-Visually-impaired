import playsound
from gtts import gTTS
import os
import speech_recognition as sr
import re
import pandas as pd
from WebScraper import get_data

get_data()
data = pd.read_csv('Corona_data_new.csv')
data['Country'][0] = "World"
data.groupby('Total Cases')

def get_total_cases(country):
    for i in range(len(data['Country'])):
        if data['Country'][i].lower() == country.lower():
            return data['Total Cases'][i]
        
def get_total_deaths(country):
    for i in range(len(data['Country'])):
        if data['Country'][i].lower() == country.lower():
            return data['Total Deaths'][i]

def get_total_recovered(country):
    for i in range(len(data['Country'])):
        if data['Country'][i].lower() == country.lower():
            return data['Total Recovered'][i]
    
def list_of_countries():
    countries = []
    for i in range(len(data['Country'])):
        countries.append(data['Country'][i].lower())
    return countries

def speak(String):
    print(String)
    tts = gTTS(text = String, lang = 'en')
    tts.save('Speech.mp3')
    playsound.playsound("Speech.mp3")
    os.remove("Speech.mp3")
      
def listen():
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
          audio = r.listen(source)
    said = ""
    try:
          said = r.recognize_google(audio)
    except Exception as e:
          print("Exception : ",str(e))
    return said.lower()

def main():
    speak("Hello, Welcome to CoronaVirus voice assistant")
    country_list = list_of_countries()
    END_PHRASE = "stop"
    
    WORLD_PATTERNS = {
					re.compile("[\w\s]+ total cases"):get_total_cases,
					re.compile("[\w\s]+ total deaths"):get_total_deaths,
					re.compile("[\w\s]+ total recovered"):get_total_recovered
					}

    COUNTRY_PATTERNS = {
					re.compile("[\w\s]+ cases [\w\s]+"):get_total_cases,
					re.compile("[\w\s]+ deaths [\w\s]+"):get_total_deaths,
                    re.compile("[\w\s]+ recovered [\w\s]+"):get_total_recovered
                        }
    while True:
        print("\nListening...")
        text = listen()
        print(text)
        result = None
        
        if "hello" in text:
            speak("Hello, what do you want to know?")
            
        if "precautions" in text:
            speak("Wash your hands often with soap and water for at least 20 seconds. Avoid touching your eyes, nose and mouth with unwashed hands. Avoid close contact with people who are sick. Cover your nose and mouth with a tissue when coughing or sneezing")
            
        if "symptoms" in text:
            speak("Difficulty breathing or shortness of breath. Chest pain or pressure. Loss of speech or movement, are the serious symptoms.")
            
        if "treatment" in text:
            speak("If you feel sick you should rest, drink plenty of fluid, and eat nutritious food. Stay in a separate room from other family members, and use a dedicated bathroom if possible. Clean and disinfect frequently touched surfaces.")
        
        if "countries in danger" in text:
            risky_countries = ' ,'.join(country_list[1:6])
            speak(risky_countries+" are the top 5 highly infected countries in the world.")
        
        if "helpline" in text:
            speak("Central Helpline Number for corona-virus: +91-11-23978046")
        
        if "safe countries" in text:
            country_list.reverse()
            safe_countries = ' ,'.join(country_list[1:6])
            country_list.reverse()
            speak(safe_countries+" are the top 5 safest countries in the world.")
            
        for pattern, func in COUNTRY_PATTERNS.items():
            if pattern.match(text):
                words = set(text.split(" "))
                for country in country_list:
                    if country in words:
                        result = func(country)
                        break

        for pattern, func in WORLD_PATTERNS.items():
            if pattern.match(text):
                result = func("World")
                break
            
        if result != None:
            speak(result)
    
        if text.find(END_PHRASE) != -1:
            speak("STAY SAFE, STAY HOME. bye")
            break
main()