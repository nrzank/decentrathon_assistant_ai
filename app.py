import requests
import streamlit as st

# URL вашего API
API_URL = "http://localhost:8000/api/endpoint/"  # Замените на ваш URL


def fetch_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Ошибка при получении данных из API.")
        return None


def main():
    st.title("Streamlit + Django REST Framework")

    # Получаем данные из API
    data = fetch_data()

    if data:
        st.write(data)  # Отображаем данные на странице


if __name__ == "_main_":
    main()
