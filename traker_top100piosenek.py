import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

import wikipedia #te 3 biblioteki poniżej służą mi do obsługi zbierania gatunków piosenek
import wptools
import json

import re

import sys
import os
from contextlib import contextmanager



CACHE_FILE = "genre_cache.json"
cache={}

@contextmanager #oszaleje tu
def suppress_stderr():
    with open(os.devnull, 'w') as devnull:
        old_stderr = sys.stderr
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stderr = old_stderr



# Ładujemy cache z pliku (jeśli istnieje)
def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return {}

# Zapisujemy cache do pliku
def save_cache(cache):
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def extract_main_artist(artist_name):
    return re.split(r'\s+(X|x|&|feat\.?|featuring)\s+', artist_name, flags=re.IGNORECASE)[0].strip()




def clean_genres(raw):
    if not raw:
        return ""
    if not isinstance(raw,str):
        raw=str(raw)
    
    # 1. Usuń szablony i nowe linie
    text = raw.replace("{{flatlist|", "").replace("{{flat list|", "").replace("}}", "")
    
    # 2. Usuń gwiazdki i spacje nadmiarowe
    text = re.sub(r"\*", "", text)
    
    # 3. Wyciągnij wszystkie [[...]] z obsługą aliasów
    matches = re.findall(r"\[\[([^]]+)\]\]", text)
    
    genres = []
    for m in matches:
        if "|" in m:
            parts = m.split("|")
            genres.append(parts[-1].strip().capitalize())
        else:
            genres.append(m.strip().capitalize())
    
    # Usuń duplikaty i połącz średnikiem
    genres = list(dict.fromkeys(genres))
    
    return "; ".join(genres)




def split_artists(artist_name):
    # Rozdzielaj po znakach X, :, , i &
    parts = re.split(r'[X:,&]', artist_name)
    # Usuń białe znaki i pustki
    artists = [p.strip() for p in parts if p.strip()]
    return artists


def get_genre(artist_name, cache):
    if artist_name in cache:
        return cache[artist_name]
    
    artists = split_artists(artist_name)
    
    for artist in artists:
        try:
            with suppress_stderr():
                page = wptools.page(artist, silent=True).get_parse()
            infobox = page.data.get('infobox', {})
            genre = (infobox.get('genre') or infobox.get('genres') or infobox.get('Genres') or infobox.get('Genre'))
            
            if genre:
                cache[artist] = genre
                return genre
            else:
                continue
                
        except Exception as e:
            pass

    cache[artist_name] = "Unknown"
    return "Unknown"
    




def get_billboard_hot100():
    url = "https://www.billboard.com/charts/hot-100"
    response = requests.get(url)
    if response.status_code != 200:
        print("Błąd pobierania strony:", response.status_code)
        return None


    soup = BeautifulSoup(response.text, 'html.parser')


    piosenki = soup.find_all('li', class_='o-chart-results-list__item')

    data = []
    rank = 1
    for song in piosenki:
        title_tag = song.find('h3', id='title-of-a-story')
        artist_tag = song.find('span', class_='c-label')
        if title_tag and artist_tag:
            title = title_tag.get_text(strip=True)
            artist = artist_tag.get_text(strip=True)
            genre=get_genre(extract_main_artist(artist), cache)
            genre=clean_genres(genre)

            if genre == '':
                genre='Unknown'

            data.append({'rank': rank, 'title': title, 'artist': artist, 'genre': genre})
            rank += 1
            if rank > 100:
                break


    return data

def save_to_csv(data):
    df = pd.DataFrame(data)
    dzisiaj = datetime.now().strftime('%Y-%m-%d')
    filename = f"billboard_got100_{dzisiaj}.csv"
    df.to_csv(filename, index=False)
    print(f"Zapisano dane do {filename}")


if __name__ == "__main__":
    cache=load_cache()
    piosenki = get_billboard_hot100()
    print("costam dziala")
    if piosenki:
        save_to_csv(piosenki)
        save_cache(cache)
        print("meow!! :3")


