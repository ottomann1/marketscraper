import requests
from bs4 import BeautifulSoup

class BlocketScraper:
    BASE_URL = "https://www.blocket.se"

    def __init__(self, search_query):
        self.search_query = search_query

    def fetch_ads(self):
        # Fetch the HTML content
        response = requests.get(f"{self.BASE_URL}/annonser/hela_sverige?q={self.search_query}")
        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup)
        
        ads = []
        # Parse HTML to find ad data
        for ad in soup.find_all("div", class_="ad-item"):
            print(ad)
            ads.append({
                "title": ad.find("h2").text,
                "price": ad.find("span", class_="price").text if ad.find("span", class_="price") else "N/A",
                "link": self.BASE_URL + ad.find("a")["href"]
            })
        print(ads)
        return ads
