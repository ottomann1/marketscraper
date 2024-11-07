from flask import Flask
from api import init_app
from db_handler import DatabaseHandler

app = Flask(__name__)

def main():
    global db_handler
    db_handler = DatabaseHandler()

    # Initialize the API routes
    init_app(app)

    # Start the Flask app
    app.run(debug=True, port=5000)

if __name__ == "__main__":
    main()
