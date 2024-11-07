from scrapers.blocket_scraper import BlocketScraper
import pandas as pd
import os

class DatabaseHandler:
    def __init__(self, filename="ads.csv"):
        self.filename = filename
        self.existing_ads = set()
        self.load_existing_ads()

    def load_existing_ads(self):
        """
        Loads existing ads from the CSV file into memory (if the file exists).
        """
        if os.path.exists(self.filename):
            try:
                df = pd.read_csv(self.filename)
                # Store links of ads currently in the CSV
                self.existing_ads = set(df["link"].tolist())
                print(f"Loaded {len(self.existing_ads)} ads from {self.filename}.")
            except Exception as e:
                print(f"Error loading existing ads: {e}")
        else:
            print(f"No existing ads file found at {self.filename}. Starting fresh.")

    def save_new_ads(self, ads):
        """
        Saves only the new ads that aren't already in the database.
        Returns the list of newly added ads.
        """
        new_ads = []
        for ad in ads:
            if ad["link"] not in self.existing_ads:
                self.existing_ads.add(ad["link"])
                new_ads.append(ad)
        return new_ads

    def save_to_csv(self, ads):
        """
        Saves ads to the CSV file. Appends new ads to the existing file.
        """
        if ads:  # Only save if there are new ads
            df = pd.DataFrame(ads)
            if os.path.exists(self.filename):
                df.to_csv(self.filename, mode='a', header=False, index=False)
            else:
                df.to_csv(self.filename, index=False)
            print(f"Saved {len(ads)} new ads to {self.filename}.")
        else:
            print("No new ads to save.")

def main():
    search_term = "laptop"
    
    blocket_scraper = BlocketScraper(search_term)
    db_handler = DatabaseHandler("ads.csv")

    # Fetch ads
    blocket_ads = blocket_scraper.fetch_ads()
    
    # Save new ads to the database
    new_ads = db_handler.save_new_ads(blocket_ads)
    
    # Save new ads to CSV
    db_handler.save_to_csv(new_ads)

def save_data(ads, filename="ads.csv"):
    df = pd.DataFrame(ads)
    df.to_csv(filename, index=False)

if __name__ == "__main__":
    main()
