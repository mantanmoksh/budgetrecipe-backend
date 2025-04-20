
import mysql.connector

def get_connection():
    try:
        return mysql.connector.connect(
            host='localhost',  # Or your database host
            user='Tanu',
            password='T@nm@yee7330817025',
            database='budget_recipes'
        )
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        #  Important:  Consider raising an exception or handling this more robustly.  For example:
        #  raise Exception("Failed to connect to database") from e
        return None # crucial: Return None in case of error
