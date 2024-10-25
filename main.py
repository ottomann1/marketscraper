from scrapers.blocket_scraper import BlocketScraper
import pandas as pd

def main():
    search_term = "laptop"
    
    blocket_scraper = BlocketScraper(search_term)

    blocket_ads = blocket_scraper.fetch_ads()

    save_data(blocket_ads, "ads.csv")

def save_data(ads, filename="ads.csv"):
    df = pd.DataFrame(ads)
    df.to_csv(filename, index=False)

if __name__ == "__main__":
    main()
