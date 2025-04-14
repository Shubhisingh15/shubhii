from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Database configuration
HOST = os.getenv('DB_HOST', 'localhost')
USER = os.getenv('DB_USER', 'root')
PASSWORD = os.getenv('DB_PASSWORD', 'shu@15')
DATABASE = os.getenv('DB_DATABASE', 'sharesphere')

# config.py
db_config = {
    'host': HOST,
    'user': USER,
    'password': PASSWORD,
    'database': DATABASE
}
