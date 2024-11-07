import pandas as pd
import os

class DatabaseHandler:
    def __init__(self, filename="ads.csv", terms_file="search_terms.csv"):
        self.ads_filename = filename
        self.terms_filename = terms_file
        self.existing_ads = set()
        self.search_terms = []
        self.load_existing_ads()
        self.load_search_terms()

    def load_existing_ads(self):
        """Load existing ads from the CSV into memory (if the file exists)."""
        if os.path.exists(self.ads_filename):
            try:
                df = pd.read_csv(self.ads_filename)
                self.existing_ads = set(df["link"].tolist())
                print(f"Loaded {len(self.existing_ads)} ads from {self.ads_filename}.")
            except Exception as e:
                print(f"Error loading existing ads: {e}")
        else:
            print(f"No existing ads file found at {self.ads_filename}. Starting fresh.")

    def load_search_terms(self):
        """Load search terms from a CSV into memory (if the file exists)."""
        if os.path.exists(self.terms_filename):
            try:
                df = pd.read_csv(self.terms_filename)
                self.search_terms = df["search_term"].tolist()
                print(f"Loaded {len(self.search_terms)} search terms from {self.terms_filename}.")
            except Exception as e:
                print(f"Error loading search terms: {e}")
        else:
            print(f"No search terms file found at {self.terms_filename}. Starting fresh.")

    def save_new_ads(self, ads):
        """Save only the new ads that aren't already in the database. Returns the list of newly added ads."""
        new_ads = []
        for ad in ads:
            print(self.existing_ads, "\n\n\n existing ads")
            print(ad, "\n\n\n new ad")
            if ad["link"] not in self.existing_ads:
                self.existing_ads.add(ad["link"])
                new_ads.append(ad)
        return new_ads

    def save_to_csv(self, ads):
        """Save ads to the CSV file. Appends new ads to the existing file."""
        if ads:  # Only save if there are new ads
            df = pd.DataFrame(ads)
            if os.path.exists(self.ads_filename):
                df.to_csv(self.ads_filename, mode='a', header=False, index=False)
            else:
                df.to_csv(self.ads_filename, index=False)
            print(f"Saved {len(ads)} new ads to {self.ads_filename}.")
        else:
            print("No new ads to save.")

    def save_search_terms(self):
        """Save search terms to the CSV file."""
        if self.search_terms:
            df = pd.DataFrame({"search_term": self.search_terms})
            df.to_csv(self.terms_filename, index=False)
            print(f"Saved {len(self.search_terms)} search terms to {self.terms_filename}.")
        else:
            print("No search terms to save.")

    def add_search_term(self, term):
        """Add a new search term."""
        if term not in self.search_terms:
            self.search_terms.append(term)
            self.save_search_terms()
            print(f"Added new search term: {term}")
        else:
            print(f"Search term '{term}' already exists.")

    def delete_search_term(self, term):
        """Delete a search term."""
        if term in self.search_terms:
            self.search_terms.remove(term)
            self.save_search_terms()
            print(f"Deleted search term: {term}")
        else:
            print(f"Search term '{term}' not found.")

    def get_all_search_terms(self):
        """Return all search terms."""
        return self.search_terms
