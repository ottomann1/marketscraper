import requests
from bs4 import BeautifulSoup

class BlocketScraper:
    BASE_URL = "https://www.blocket.se"

    def __init__(self, search_query):
        self.search_query = search_query

    def fetch_ads(self):
        response = requests.get(f"{self.BASE_URL}/annonser/hela_sverige?q={self.search_query}&sort=date")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        ads = []

        for ad in soup.find_all("div", class_="styled__Wrapper-sc-1kpvi4z-0 iQpUlz"):
            title = ad.find("h2").text
            price_text = ad.find("div", class_="Price__StyledPrice-sc-1v2maoc-1 lbJRcp").text
            # Convert price to integer
            price = int(price_text.replace("kr", "").strip().replace(" ", ""))
            link = self.BASE_URL + ad.find("h2").find("a")["href"]
            
            ads.append({
                "title": title,
                "price": price,
                "link": link
            })
            print(ad, "\n\n\n NEW AD \n\n\n")
        print("ALL ADS BELOW \n\n\n",ads, "\n\n\n ALL ADS ABOVE")
        return ads
