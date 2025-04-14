from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from config import db_config
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Home (Redirect to login if not logged in)
@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                       (username, email, password))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')

    return render_template('login.html')

# Dashboard (only accessible when logged in)
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (name, email, message) VALUES (%s, %s, %s)",
                       (name, email, message))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Your message has been sent!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

# Add other routes similarly and protect them:
@app.route('/categories')
def categories():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('categories.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
#recipe
@app.route('/recipes')
def recipes():
    recipe_data = [
        {
            "title": "Spaghetti Carbonara",
            "user_id": "user123",
            "description": "A classic Italian pasta dish with eggs, cheese, pancetta, and pepper.",
            "steps": [
                "Boil pasta until al dente.",
                "Cook pancetta in a pan.",
                "Mix eggs, cheese, and pepper in a bowl.",
                "Combine pasta, pancetta, and egg mixture.",
                "Serve immediately with extra cheese."
            ],
            "image_url": "https://www.allrecipes.com/thmb/Vg2cRidr2zcYhWGvPD8M18xM_WY=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/11973-spaghetti-carbonara-ii-DDMFS-4x3-6edea51e421e4457ac0c3269f3be5157.jpg",
            "tutorial_url": "https://www.youtube.com/watch?v=3AAdKl1UYZs"
        },
        {
            "title": "Avocado Toast",
            "user_id": "greenchef45",
            "description": "Simple and delicious toast topped with creamy avocado and seasoning.",
            "steps": [
                "Toast bread slices.",
                "Mash avocado with salt and lemon juice.",
                "Spread avocado on toast.",
                "Top with eggs or tomatoes.",
                "Enjoy immediately."
            ],
            "image_url": "https://img.freepik.com/free-photo/avocado-open-toast-with-avocado-slices-lemon-flax-seeds-sesame-seeds-black-bread-slices-top-view_2831-797.jpg",
            "tutorial_url": "https://www.youtube.com/watch?v=I0t8ZAhb8lQ"
        },
        {
            "title": "Homemade Pizza",
            "user_id": "pizzalover77",
            "description": "Make your own pizza with fresh ingredients and toppings.",
            "steps": [
                "Preheat oven to 220°C (430°F).",
                "Roll out pizza dough.",
                "Spread tomato sauce and add toppings.",
                "Bake 12–15 min until golden.",
                "Let cool slightly before serving."
            ],
            "image_url": "https://www.allrecipes.com/thmb/9UTj7kZBJDqory0cdEv_bw6Ef_0=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/48727-Mikes-homemade-pizza-DDMFS-beauty-2x1-BG-2976-d5926c9253d3486bbb8a985172604291.jpg",
            "tutorial_url": "https://www.youtube.com/watch?v=UQHfLufNL-k"
        },
        {
            "title": "Chocolate Brownies",
            "user_id": "bakequeen92",
            "description": "Rich and fudgy brownies perfect for dessert lovers.",
            "steps": [
                "Preheat oven to 175°C (350°F).",
                "Melt butter and mix with sugar.",
                "Add eggs and vanilla extract.",
                "Mix in cocoa, flour, and baking powder.",
                "Bake for 25–30 minutes."
            ],
            "image_url": "https://img.taste.com.au/kdMbjArS/taste/2010/01/chocolate-brownies-118925-2.jpg",
            "tutorial_url": "https://www.youtube.com/watch?v=KETPZPm6148"
        }
    ]
    return render_template('recipes.html', recipes=recipe_data)

