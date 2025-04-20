from flask import Flask, request, jsonify
from db import get_connection
from flask_cors import CORS
import traceback  # Import traceback for detailed error logging

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Signup
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data['username']
    password = data['password']

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        conn.rollback()
        # Log the error for debugging
        print(f"Error in signup: {e}")
        print(traceback.format_exc()) # Print detailed traceback
        return jsonify({'status': 'error', 'message': 'Username already exists'}), 409
    finally:
        conn.close()

# Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        if user:
            return jsonify({'status': 'success', 'user_id': user['id']})
        else:
            return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401
    except Exception as e:
        print(f"Error in login: {e}")
        print(traceback.format_exc())
        return jsonify({'status': 'error', 'message': 'Database error'}), 500
    finally:
        conn.close()

# Get recipes by budget
@app.route('/recipes', methods=['GET'])
def get_recipes():
    budget = request.args.get('budget', type=int)
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM recipes WHERE price <= %s", (budget,))
        recipes = cursor.fetchall()
        return jsonify(recipes)
    except Exception as e:
        print(f"Error in get_recipes: {e}")
        print(traceback.format_exc())
        return jsonify({'status': 'error', 'message': 'Failed to fetch recipes'}), 500
    finally:
        conn.close()

# Increment favourites
@app.route('/favourite', methods=['POST'])
def favourite():
    try:
        recipe_id = request.json['recipe_id']
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE recipes SET favourites = favourites + 1 WHERE id = %s", (recipe_id,))
        conn.commit()
        conn.close()  # Ensure connection is closed *before* returning
        return jsonify({'status': 'success'})
    except Exception as e:
        conn.rollback()
        print(f"Error in favourite: {e}")
        print(traceback.format_exc())
        return jsonify({'status': 'error', 'message': 'Failed to update favourites'}), 500
    finally:
        if conn: # Check if connection was established
           conn.close()

if __name__ == '__main__':
    app.run(debug=True)
