import sys
import requests
import json
from bs4 import BeautifulSoup
import os

def fetch_anime_data(aid):
    url = f"http://api.anidb.net:9001/httpapi?request=anime&client=pobo&clientver=1&protover=1&aid={aid}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch data for AID {aid}")

def parse_anime_data(xml_content):
    soup = BeautifulSoup(xml_content, 'lxml-xml')

    # Find all episodes with epno type="1"
    episodes = soup.find_all('episode', epno={'type': '1'})

    # Extract and format details of each episode
    episode_details = []
    for episode in episodes:
        epno = episode.find('epno').text
        length = episode.find('length').text
        airdate = episode.find('airdate').text
        title_ja = episode.find('title', {'xml:lang': 'ja'}).text
        title_en = episode.find('title', {'xml:lang': 'en'}).text
        title_romaji = episode.find('title', {'xml:lang': 'x-jat'}).text if episode.find('title', {'xml:lang': 'x-jat'}) else ''

        episode_details.append({
            "episode_number": int(epno),
            "name": f"{title_en} ( {title_ja} • {title_romaji})",
            "date_upload": f"{airdate}T00:00:00",
            "scanlator": f"Episode {epno} • {length}"
        })

    return episode_details

def save_to_json(data, aid, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    filename = os.path.join(output_dir, f"anime_{aid}_episodes.json")
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {filename}")

def main(aid, output_dir):
    xml_content = fetch_anime_data(aid)
    episode_details = parse_anime_data(xml_content)
    save_to_json(episode_details, aid, output_dir)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scrape_anime.py <aid> [output_dir]")
        sys.exit(1)
    aid = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else '.'
    main(aid, output_dir)
