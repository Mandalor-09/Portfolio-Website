from flask import Flask, jsonify, request, render_template, url_for, redirect
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'database.db'  # SQLite database file

# Function to get database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Enables dictionary-like row access
    return conn

# Create tables if they don't exist
def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Project (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                section TEXT NOT NULL,
                desription TEXT,  
                tech_used TEXT,
                github TEXT,
                demo TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Submission (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL
            )
        ''')
        conn.commit()

@app.route('/projects', methods=['GET'])
def get_projects():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Project")
    projects = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in projects])

@app.route('/projects', methods=['POST'])
def add_project():
    data = request.json  # Get JSON data from the request

    # Check if project name already exists
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Project WHERE name = ?", (data['name'],))
    project_exists = cursor.fetchone()

    if project_exists:
        return jsonify({"error": "Project with this name already exists!"}), 400

    cursor.execute('''
        INSERT INTO Project (name, section, desription, tech_used, github, demo)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (data['name'], data['section'], data['desription'], data['tech_used'], data['github'], data['demo']))
    
    conn.commit()
    conn.close()
    return jsonify({"message": "Project added successfully!"}), 201

@app.route('/', methods=['GET', 'POST'])
def home():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        cursor.execute("INSERT INTO Submission (name, email, message) VALUES (?, ?, ?)", (name, email, message))
        conn.commit()
        conn.close()
        return redirect(url_for('thank_you'))

    category = request.args.get('category', 'all')

    if category == 'all':
        cursor.execute("SELECT * FROM Project LIMIT 3")
    else:
        cursor.execute("SELECT * FROM Project WHERE section = ? LIMIT 3", (category,))
    
    project_list = cursor.fetchall()
    cursor.execute("SELECT DISTINCT section FROM Project")
    sections = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return render_template('index.html', project_list=project_list, sections=sections, selected_category=category)

@app.route('/thank-you')
def thank_you():
    return 'Thank You. You Will Be Contacted Soon.'

@app.route('/submissions', methods=['GET'])
def get_submissions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Submission")
    submissions = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in submissions])

if __name__ == '__main__':
    init_db()  # Ensure tables are created before running
    app.run(debug=True)
