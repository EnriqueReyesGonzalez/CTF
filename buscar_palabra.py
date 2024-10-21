import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import deque

def is_web_page(content_type):
    """HTML?"""
    return 'text/html' in content_type

def find_word_in_site(base_url, search_word):
    visited = set()
    queue = deque([base_url])

    while queue:
        url = queue.popleft()
        if url in visited:
            continue

        try:
            response = requests.get(url)
            response.raise_for_status()  # Lanza un error si la solicitud falla

            # Si no es una pagina web, fuera
            if not is_web_page(response.headers.get('Content-Type', '')):
                print(f'No pagina web: {url}')
                continue

            visited.add(url)

            # Comprobar la palabra en la pagina
            if search_word.lower() in response.text.lower():
                print(f'Palabra encontrada en: {url}')

            # Extractor enlaces
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a', href=True):
                full_url = urljoin(base_url, link['href'])
                if full_url.startswith(base_url) and full_url not in visited:
                    queue.append(full_url)

        except requests.exceptions.RequestException as e:
            print(f'Error en {url}: {e}')

if __name__ == "__main__":
    
    base_url = 'https://esi.uclm.es/' 
    search_word = 'distribución'  

    find_word_in_site(base_url, search_word)
