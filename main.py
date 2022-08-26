from random import shuffle

import pyttsx3
import speech_recognition as speech_rec

from requests import get
from bs4 import BeautifulSoup

engine = pyttsx3.init()
voices = engine.getProperty('voices') 
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.167 YaBrowser/22.7.3.822 Yowser/2.5 Safari/537.36'}



def speak_text(input_data: str) -> None:
    engine.say(input_data)
    engine.runAndWait()
    engine.stop()


def search_synonym(query: str) -> None:
    synonyms_html = get(f'https://sinonim.org/s/{query}#f', headers=headers)
    parse = BeautifulSoup(synonyms_html.text, 'html.parser')

    synonym_list_checked = []

    synonym_table_parse = parse.find('table')
    if not synonym_table_parse is None:

        tr_all = synonym_table_parse.find_all('tr')
        for tr in tr_all:
            synonym_list = tr.find_all('td')

            if synonym_list is None:
                continue

            if len(synonym_list) < 2:
                continue

            synonym_format = synonym_list[1].text
            synonym_fix = synonym_format[:synonym_format.find('(')].strip()
            synonym_list_checked.append(synonym_fix)

    if len(synonym_list_checked) == 0:
        print(f'Синонимов к слову {query} не нашлось. Возможно запрос введён некорректно.')
        speak_text(f'Синонимов к слову {query} не нашлось. Возможно запрос введён некорректно.')
    else:
        if len(synonym_list_checked) > 5:
            shuffle(synonym_list_checked)
            synonym_list_checked = synonym_list_checked[:len(synonym_list_checked)-(len(synonym_list_checked)-5)]

        synonyms_response = ''
        for synonym in synonym_list_checked:
            synonyms_response += synonym + ', '
        
        print(f'{len(synonym_list_checked)} найденных синонимов к слову {query}: {synonyms_response}')
        speak_text(f'{len(synonym_list_checked)} найденных синонимов к слову {query}: {synonyms_response}')


def listen() -> None:
    recognazer = speech_rec.Recognizer()
    with speech_rec.Microphone() as source:
        recognazer.pause_threshold = 0.5
        recognazer.adjust_for_ambient_noise(source)
        audio = recognazer.listen(source)

    try:
        task = recognazer.recognize_google(audio, language='ru-RU').lower()
    except speech_rec.UnknownValueError:
        speak_text('че')
        task = listen()

    return task

def processing_commands(task) -> None:
    print(task)

while True:
    processing_commands(listen())