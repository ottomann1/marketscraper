from flask import Flask
from api import init_app, scrape_ads
from db.db_handler import DatabaseHandler
import threading
import time

app = Flask(__name__)

def periodic_scraping():
    """Run the scrape function periodically every hour."""
    while True:
        print("Running periodic scrape...")
        scrape_ads(db_handler)
        time.sleep(3600)

def main():
    global db_handler
    db_handler = DatabaseHandler()  # Initialize db_handler here

    init_app(app, db_handler)  # Pass db_handler to init_app for access in api.py

    thread = threading.Thread(target=periodic_scraping, daemon=True)
    thread.start()
 
    app.run(debug=True, port=5000)

if __name__ == "__main__":
    main()

