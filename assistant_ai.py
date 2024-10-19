import requests
import os
import streamlit as st
from dotenv import load_dotenv
import json

# Загружаем переменные окружения
load_dotenv()

# Получаем ключи API из переменных окружения
gemini_api_key = os.getenv('GEMINI_API_KEY')
wolfram_api_key = os.getenv('WOLFRAM_API_KEY')
if not gemini_api_key or not wolfram_api_key:
    st.error("Необходим API ключ для Gemini и Wolfram Alpha. Убедитесь, что переменные окружения установлены.")
    st.stop()

# URL для API
gemini_url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={gemini_api_key}'
wolfram_url = 'http://api.wolframalpha.com/v2/query'


# Функция для классификации предмета запроса
def classify_subject(query):
    prompt = f"""Определите предмет, к которому относится следующий запрос: "{query}"
    Выберите один из следующих предметов: Математика, Физика, Химия, История, Биология, Литература, Программирование, Другое.
    Верните только название предмета без дополнительных пояснений."""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.1, "topP": 1, "topK": 1, "maxOutputTokens": 1000}
    }

    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(gemini_url, headers=headers, json=payload)
        if response.status_code == 200:
            response_json = response.json()
            if 'candidates' in response_json and response_json['candidates']:
                return response_json['candidates'][0]['content']['parts'][0]['text'].strip()
        st.write("Не удалось определить предмет, используется 'Другое'")
        return "Другое"
    except Exception as e:
        st.write(f"Ошибка при классификации предмета: {e}")
        return "Другое"

# Функция для получения ответа от Wolfram Alpha API
def check_wolfram(query):
    params = {
        'input': query,
        'format': 'plaintext',
        'output': 'JSON',
        'apikey': wolfram_api_key
    }

    try:
        response = requests.get(wolfram_url, params=params)
        if response.status_code == 200:
            response_json = response.json()
            pods = response_json.get('queryresult', {}).get('pods', [])
            results = []

            for pod in pods:
                title = pod.get('title', 'Результат')
                subpods = pod.get('subpods', [])
                for subpod in subpods:
                    if 'plaintext' in subpod and subpod['plaintext']:
                        results.append(f"{title}: {subpod['plaintext']}")

            return "\n".join(results)
        return "Не удалось получить ответ от Wolfram Alpha."
    except Exception as e:
        st.write(f"Ошибка при запросе к Wolfram Alpha API: {e}")
        return "Ошибка при запросе к Wolfram Alpha API."

# Функция для получения ответа от Gemini API
def check_gemini(context):
    payload = {
        "contents": [{"parts": [{"text": context}]}],
        "generationConfig": {"temperature": 0.7, "topP": 1, "topK": 1, "maxOutputTokens": 2048}
    }

    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(gemini_url, headers=headers, json=payload)
        if response.status_code == 200:
            response_json = response.json()
            if 'candidates' in response_json and response_json['candidates']:
                return response_json['candidates'][0]['content']['parts'][0]['text'].strip()
        return "Извините, не удалось получить ответ от Gemini API."
    except Exception as e:
        return f"Ошибка при запросе к Gemini API: {e}"

# Инициализация session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'clear_input' not in st.session_state:
    st.session_state.clear_input = False

# Интерфейс
st.title("AI Ассистент для обучения")

# Отображение истории
for i, entry in enumerate(st.session_state.history):
    st.markdown(f"*Вопрос {i + 1}:* {entry['question']}")
    st.markdown(f"*Ответ {i + 1}:* {entry['answer']}")

# Функция для отправки запроса
def submit_query():
    user_query = st.session_state.user_query
    if user_query.strip():
        subject = classify_subject(user_query)
        st.write(f"Определенный предмет: {subject}")

        if subject in ['Математика', 'Физика', 'Химия', 'История', 'Программирование', 'Литература']:
            text_response = check_wolfram(user_query)
            st.write("Ответ Wolfram Alpha:", text_response)

            if text_response.strip():
                AI_response = check_gemini(
                    f"Предмет: {subject}\n\nВопрос: {user_query}\n\nИнформация от Wolfram Alpha: {text_response}\n\nПожалуйста, дайте подробный ответ на вопрос, используя эту информацию.")
            else:
                AI_response = check_gemini(
                    f"Предмет: {subject}\n\nВопрос: {user_query}\n\nК сожалению, Wolfram Alpha не предоставил текстовой информации. Пожалуйста, дайте ответ на основе вашей базы знаний.")
        else:
            AI_response = check_gemini(f"Предмет: {subject}\n\nВопрос: {user_query}")

        st.write("Финальный ответ:", AI_response)
        st.session_state.history.append({"question": user_query, "answer": AI_response})
        st.session_state.clear_input = True

# Поле для ввода вопроса
if st.session_state.clear_input:
    st.session_state.user_query = ""
    st.session_state.clear_input = False

user_query = st.text_input('Введите ваш запрос:', key='user_query')

# Кнопка для отправки запроса
if st.button('Отправить запрос'):
    submit_query()
    st.rerun()