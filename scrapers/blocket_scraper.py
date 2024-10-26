import requests
from bs4 import BeautifulSoup

class BlocketScraper:
    BASE_URL = "https://www.blocket.se"

    def __init__(self, search_query):
        self.search_query = search_query

    def fetch_ads(self):
        response = requests.get(f"{self.BASE_URL}/annonser/hela_sverige?q={self.search_query}")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        ads = []

        for ad in soup.find_all("div", class_="styled__Wrapper-sc-1kpvi4z-0 iQpUlz"):
            ads.append({
                "title": ad.find("h2").text,
                "price": ad.find("div", class_="Price__StyledPrice-sc-1v2maoc-1 lbJRcp").text,
                "link": self.BASE_URL + ad.find("a")["href"]
            })
        return ads
