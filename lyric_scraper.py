import requests
from bs4 import BeautifulSoup
import re

def get_song_links(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        song_links = soup.find_all('a', href=re.compile(r'/lyrics/maroon5/.*?\.html'))
        song_urls = [link['href'] for link in song_links]
        return song_urls
    else:
        print("Failed to fetch data:", response.status_code)
        return None

def scrape_lyrics(url):
    response = requests.get(url)
    if response.status_code == 200:
        lyrics_matches = re.findall(r'<!-- Usage of .* is .* -->(.*?)<!-- MxM banner -->', response.text, re.DOTALL)
        all_lyrics = []
        for match in lyrics_matches:
            lyrics_text = re.sub(r'<.*?>', '', match)
            lyrics_text = lyrics_text.replace('\n', '').replace('\r', '')
            all_lyrics.append(lyrics_text.strip())
        return all_lyrics
    else:
        print("Failed to fetch data:", response.status_code)
        return None

# URL of the Maroon 5 lyrics page
url = 'https://www.azlyrics.com/m/maroon5.html'
# Get the links to individual song pages
song_urls = get_song_links(url)

if song_urls:
    all_lyrics = []
    for song_url in song_urls:
        # Scrape the lyrics for each song
        lyrics = scrape_lyrics('https://www.azlyrics.com' + song_url)
        if lyrics:
            all_lyrics.extend(lyrics)

    # Write the lyrics to a text file
    with open('maroon5_lyrics.txt', 'w', encoding='utf-8') as file:
        for lyrics in all_lyrics:
            file.write(lyrics + '\n\n')
    print("Lyrics saved to 'maroon5_lyrics.txt'")
else:
    print("No song links found.")
