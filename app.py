from flask import Flask, request, jsonify
from flask_cors import CORS
from db import get_connection
import os

app = Flask(__name__)
CORS(app)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",(data['username'], data['email'], data['password']))

        conn.commit()
        return jsonify({'status': 'success'})
    except:
        conn.rollback()
        return jsonify({'status': 'error'}), 409
    finally:
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (data['username'], data['password']))
    user = cursor.fetchone()
    conn.close()
    if user:
        return jsonify({'status': 'success', 'user_id': user['id']})
    else:
        return jsonify({'status': 'error'}), 401

@app.route('/recipes', methods=['GET'])
def recipes():
    budget = request.args.get('budget', type=float)
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM recipes WHERE price <= %s", (budget,))
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

@app.route('/favourite', methods=['POST'])
def add_favourite():
    data = request.json
    user_id = data['user_id']
    recipe_id = data['recipe_id']
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO favourites (user_id, recipe_id) VALUES (%s, %s)", (user_id, recipe_id))
        conn.commit()
        return jsonify({'status': 'success'})
    except:
        conn.rollback()
        return jsonify({'status': 'error'}), 500
    finally:
        conn.close()

@app.route('/favourites', methods=['GET'])
def get_favourites():
    user_id = request.args.get('user_id')
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.* FROM recipes r
        JOIN favourites f ON r.id = f.recipe_id
        WHERE f.user_id = %s
    """, (user_id,))
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
