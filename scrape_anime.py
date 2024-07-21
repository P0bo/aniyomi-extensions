# scrape_anime.py
import sys
import requests
from bs4 import BeautifulSoup

def fetch_anime_data(aid):
    url = f"http://api.anidb.net:9001/httpapi?request=anime&client=pobo&clientver=1&protover=1&aid={aid}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch data for AID {aid}")

def parse_anime_data(xml_content):
    soup = BeautifulSoup(xml_content, 'xml')

    # Find all episodes with epno type="1"
    episodes = soup.find_all('episode', epno={'type': '1'})

    # Extract and print details of each episode
    episode_details = []
    for episode in episodes:
        epno = episode.find('epno').text
        length = episode.find('length').text
        airdate = episode.find('airdate').text
        title_ja = episode.find('title', {'xml:lang': 'ja'}).text
        title_en = episode.find('title', {'xml:lang': 'en'}).text
        rating = episode.find('rating').text if episode.find('rating') else 'N/A'
        
        episode_details.append({
            "epno": epno,
            "length": length,
            "airdate": airdate,
            "title_ja": title_ja,
            "title_en": title_en,
            "rating": rating
        })

    return episode_details

def main(aid):
    xml_content = fetch_anime_data(aid)
    episode_details = parse_anime_data(xml_content)
    
    for detail in episode_details:
        print(f"Episode {detail['epno']}:")
        print(f"  Length: {detail['length']} minutes")
        print(f"  Airdate: {detail['airdate']}")
        print(f"  Title (Japanese): {detail['title_ja']}")
        print(f"  Title (English): {detail['title_en']}")
        print(f"  Rating: {detail['rating']}")
        print()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scrape_anime.py <aid>")
        sys.exit(1)
    aid = sys.argv[1]
    main(aid)
