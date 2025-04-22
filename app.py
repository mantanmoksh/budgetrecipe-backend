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

    # Query for recipes based on the budget
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, price FROM recipes WHERE price <= %s", (budget,))
    data = cursor.fetchall()
    conn.close()

    # Predefined descriptions, image URLs, and specific recipe pages for some recipe names
    descriptions = {
        "Besan Chilla": "A healthy and tasty South Indian breakfast dish made with semolina.",
        "Aloo Paratha": "A delicious stuffed Indian flatbread filled with spiced mashed potatoes.",
        "Paneer Butter Masala": "A rich and creamy tomato-based curry with soft paneer cubes.",
        "Veg Biryani": "A fragrant rice dish cooked with spices and mixed vegetables.",
        "Chickpea Spinach Curry": "Hearty, nutritious chickpea and spinach curry.",
        "Gutti Vankaya Curry": "Stuffed brinjal curry with rich spices.",
        "Palak Paneer": "A North Indian curry made with pureed spinach and paneer cubes.",
        "Dal Makhani": "Creamy, buttery, rich, slow-cooked lentil curry.",
        "Chole Bhature": "A classic Punjabi dish of spicy chickpeas served with deep-fried bread.",
        "Veg Pulao": "Fragrant rice with spiced vegetables.",
        "Aloo tikki": "Crispy spiced potato patties, delicious snack.",
        "Veg Spring rolls": "Crispy, stuffed, savory, fried, delicious.",
        "Veg Grilled Sandwich": "Fresh, crunchy, cheesy, healthy, delicious sandwich.",
        "Veg Kofta Curry": "Spiced vegetable balls in rich gravy.",
        "White Sause Pasta": "Creamy, cheesy, garlic-flavored pasta delight.",
        "Aloo Fry Curry": "Spiced, flavorful, potato-based Indian curry.",
        "Bendi Fry": "Crispy, spiced, stir-fried okra delight.",
        "Veg Noodles": "Spicy, stir-fried, flavorful veggie noodles.",
        "Dhokla": "Soft, spongy, steamed savory gram flour cake."
    }

    images = {
        "Besan Chilla": "https://i.pinimg.com/736x/93/c5/49/93c5492c509282be6b7cef80ed2e7179.jpg",
        "Aloo Paratha": "https://i0.wp.com/khaddoroshik.com/wp-content/uploads/2023/12/Aloo-Paratha-Recipe.webp?w=1024&ssl=1",
        "Paneer Butter Masala": "https://i.pinimg.com/736x/d6/be/99/d6be99b3ffc8033087e466883f7459f1.jpg",
        "Veg Biryani": "https://i.pinimg.com/736x/95/80/7b/95807ba96c11e2387e909767c19f68ff.jpg",
        "Chickpea Spinach Curry": "https://i.pinimg.com/736x/d1/c1/61/d1c161fb52b8002e2a835305f5c0f8fe.jpg",
        "Gutti Vankaya Curry": "https://i.pinimg.com/736x/38/e2/77/38e277f870defd6f3d7d13fb722de888.jpg",
        "Palak Paneer": "https://i.pinimg.com/736x/2f/5e/ae/2f5eae6b7d5badd5dbeee57e81d28a84.jpg",
        "Dal Makhani": "https://i.pinimg.com/736x/2a/c6/57/2ac657e8a320ac35ac5b7c67c339ea1d.jpg",
        "Chole Bhature": "https://i.pinimg.com/736x/f5/9c/9a/f59c9a7f63c2cd4bd587f3de73f184a4.jpg",
        "Veg Pulao": "https://i.pinimg.com/736x/18/c5/8d/18c58d13627917fb60d39d2ce019d6a1.jpg",
        "Aloo tikki": "https://i.pinimg.com/736x/cf/e2/33/cfe233928aa6d63b982ddfd048cee847.jpg",
        "Veg Spring rolls": "https://i.pinimg.com/736x/29/41/a6/2941a6153669acb5a03c375fd50c54c4.jpg",
        "Veg Grilled Sandwich": "https://i.pinimg.com/736x/32/e6/3a/32e63adb3a5644f3ae88b86e98187286.jpg",
        "Veg Kofta Curry": "https://i.pinimg.com/736x/77/6b/6d/776b6d49ec2ddc58033db5786ee135f2.jpg",
        "White Sause Pasta": "https://i.pinimg.com/736x/e8/68/c8/e868c8f4d0928bcb470fcf4e69c212cc.jpg",
        "Aloo Fry Curry": "https://i.pinimg.com/736x/80/e2/01/80e2014e953fc0de1c980a05982250fc.jpg",
        "Bendi Fry": "https://i.pinimg.com/736x/52/d3/7b/52d37bd575f08565db4e97c8c2ade53d.jpg",
        "Veg Noodles": "https://i.pinimg.com/736x/ae/a4/36/aea4369b1d071a4382b4b909669c6814.jpg",
        "Dhokla": "https://i.pinimg.com/736x/3e/e6/60/3ee660d8ddfa8dc26b1e975f93c60648.jpg"
    }

    recipe_pages = {
        "Besan Chilla": "/besanchilla.html",
        "Aloo Paratha": "/alooparatha.html",
        "Paneer Butter Masala": "/paneerbuttermasala.html",
        "Veg Biryani": "/vegbiryani.html",
        "Chickpea Spinach Curry": "/chickpeaspinach.html",
        "Gutti Vankaya Curry": "/guttivankaya.html",
        "Palak Paneer": "/palakpaneer.html",
        "Dal Makhani": "/dalmakhani.html",
        "Chole Bhature": "/cholebhature.html",
        "Veg Pulao": "/vegpulav.html",
        "Aloo tikki": "/alootikki.html",
        "Veg Spring rolls": "/vegspringrolls.html",
        "Veg Grilled Sandwich": "/veggrillsandwich.html",
        "Veg Kofta Curry": "/vegkofta.html",
        "White Sause Pasta": "/whitesaucepasta.html",
        "Aloo Fry Curry": "/aloofry.html",
        "Bendi Fry": "/bendifry.html",
        "Veg Noodles": "/vegnoodles.html",
        "Dhokla": "/dhokla.html"
    }

    # Categorize recipes and enhance with metadata
    for recipe in data:
        name = recipe['name']
        name_lower = name.lower()

        # Assign category (optional: improve logic based on actual categories)
        if 'breakfast' in name_lower:
            recipe['category'] = 'Breakfast'
        elif 'lunch' in name_lower:
            recipe['category'] = 'Lunch'
        elif 'dinner' in name_lower:
            recipe['category'] = 'Dinner'
        elif 'dessert' in name_lower:
            recipe['category'] = 'Dessert'
        else:
            recipe['category'] = 'Other'

        recipe['description'] = descriptions.get(name, "A delicious recipe.")
        recipe['image_url'] = images.get(name, "https://via.placeholder.com/150")
        recipe['recipe_page'] = recipe_pages.get(name, "/defaultrecipe.html")

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
