from flask import Flask
from api import init_app, scrape_ads
from db_handler import DatabaseHandler
import threading
import time

app = Flask(__name__)

def periodic_scraping():
    """Run the scrape function periodically every hour."""
    while True:
        print("Running periodic scrape...")
        scrape_ads()
        time.sleep(3600)

def main():
    global db_handler
    db_handler = DatabaseHandler()

    # Initialize the API routes
    init_app(app)
    
    thread = threading.Thread(target=periodic_scraping, daemon=True)
    thread.start()
 
    # Start the Flask app
    app.run(debug=True, port=5000)

if __name__ == "__main__":
    main()
