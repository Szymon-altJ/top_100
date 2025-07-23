import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

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
            data.append({'rank': rank, 'title': title, 'artist': artist})
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
    piosenki = get_billboard_hot100()
    print("costam dziala")
    if piosenki:
        save_to_csv(piosenki)
        print("meow!!")
