import os
import pymysql
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Function to get DB connection
def get_connection():
    # Retrieve credentials from environment variables
    host = os.getenv("DB_HOST", "switchyard.proxy.rlwy.net")
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "vqUeTTDMFoOLPdJnNTHSwRuyHyeTKguZ")
    db = os.getenv("DB_NAME", "railway")
    port = int(os.getenv("DB_PORT", 28897))  # Make sure to set the port number

    # Establish a connection using pymysql
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=db,
        port=port,
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection
