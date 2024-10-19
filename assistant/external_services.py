import requests



# Запрос к Gemini API
def search_gemini(query):
    url = f"https://api.gemini.com/search?query={query}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {}

# Запрос к Wikipedia API
def search_wikipedia(query):
    url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={query}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {}



def get_similar_queries(query):
    url = f"https://api.similarqueries.com/search?query={query}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('similar_queries', [])
    return []