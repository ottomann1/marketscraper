from flask import request, jsonify
from db_handler import DatabaseHandler
from scrapers.blocket_scraper import BlocketScraper

db_handler = DatabaseHandler()

def init_app(app):
    """Initialize all the routes in the Flask app."""
    
    @app.route('/search_terms', methods=['GET'])
    def get_search_terms():
        terms = db_handler.get_all_search_terms()
        return jsonify(terms)

    @app.route('/search_terms', methods=['POST'])
    def add_search_term():
        term = request.json
        if term:
            db_handler.add_search_term(term.get('search_term'))
            return jsonify({"message": "Search term added"}), 201
        else:
            return jsonify({"message": "No search term provided"}), 400

    @app.route('/search_terms/<term>', methods=['DELETE'])
    def delete_search_term(term):
        db_handler.delete_search_term(term)
        return jsonify({"message": "Search term deleted"}), 200

    @app.route('/scrape', methods=['GET'])
    def scrape():
        ads = []
        for term in db_handler.get_all_search_terms():
            blocket_scraper = BlocketScraper(term)
            blocket_ads = blocket_scraper.fetch_ads()
            print(blocket_ads, "\n\n\n blocket ads")
            new_ads = db_handler.save_new_ads(blocket_ads)
            print(new_ads, "\n\n\n new ads")
            ads.extend(new_ads)
            print(ads)
        db_handler.save_to_csv(ads)
        return jsonify({"message": f"Scraped {len(ads)} new ads"}), 200
