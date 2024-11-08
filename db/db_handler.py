import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base, Ad, SearchTerm

class DatabaseHandler:
    def __init__(self, db_url="postgresql://user:password@localhost:5432/marketscraper"):
        """Initialize the database handler."""
        self.db_url = db_url
        self.engine = create_engine(self.db_url, echo=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        self.load_existing_ads()
        self.load_search_terms()

    def load_existing_ads(self):
        """Load existing ads from the database into memory."""
        try:
            ads = self.session.query(Ad).all()
            self.existing_ads = {ad.link for ad in ads}
            print(f"Loaded {len(self.existing_ads)} ads from the database.")
        except Exception as e:
            print(f"Error loading existing ads: {e}")
            self.existing_ads = set()

    def load_search_terms(self):
        """Load search terms from the database into memory."""
        try:
            terms = self.session.query(SearchTerm).all()
            self.search_terms = [term.search_term for term in terms]
            print(f"Loaded {len(self.search_terms)} search terms from the database.")
        except Exception as e:
            print(f"Error loading search terms: {e}")
            self.search_terms = []

    def save_new_ads(self, ads, search_term):
        """Save only the new ads that aren't already in the database."""
        new_ads = []
        
        for ad in ads:
            if ad["link"] not in self.existing_ads:
                ad["search_term"] = search_term
                new_ad = Ad(**ad)
                self.session.add(new_ad)
                self.existing_ads.add(ad["link"])
                new_ads.append(ad)
        self.session.commit()
        print(f"Saved {len(new_ads)} new ads.")
        return new_ads

    def add_search_term(self, term):
        """Add a new search term to the database."""
        if term not in self.search_terms:
            new_term = SearchTerm(search_term=term)
            self.session.add(new_term)
            self.search_terms.append(term)
            self.session.commit()
            print(f"Added new search term: {term}")
        else:
            print(f"Search term '{term}' already exists.")

    def delete_search_term(self, term):
        """Delete a search term from the database."""
        if term in self.search_terms:
            term_to_delete = self.session.query(SearchTerm).filter_by(search_term=term).first()
            if term_to_delete:
                self.session.delete(term_to_delete)
                self.search_terms.remove(term)
                self.session.commit()
                print(f"Deleted search term: {term}")
        else:
            print(f"Search term '{term}' not found.")

    def get_all_search_terms(self):
        """Return all search terms."""
        return self.search_terms
