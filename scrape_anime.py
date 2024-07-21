# scrape_anime.py
from bs4 import BeautifulSoup

# Load the XML content from the file
with open('anime.xml', 'r', encoding='utf-8') as file:
    xml_content = file.read()

# Parse the XML content
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

# Print or save the episode details
for detail in episode_details:
    print(f"Episode {detail['epno']}:")
    print(f"  Length: {detail['length']} minutes")
    print(f"  Airdate: {detail['airdate']}")
    print(f"  Title (Japanese): {detail['title_ja']}")
    print(f"  Title (English): {detail['title_en']}")
    print(f"  Rating: {detail['rating']}")
    print()
