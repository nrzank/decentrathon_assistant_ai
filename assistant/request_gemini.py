import requests

def get_answer_from_gemini(question, api_url, api_key):

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'

    }

    payload = {
        'question': question
    }

    response = requests.post(api_url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()

    else:
        return None

    