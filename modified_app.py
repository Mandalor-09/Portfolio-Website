from flask import Flask, jsonify, request, render_template, url_for, redirect
import mysql.connector
import os
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

app = Flask(__name__)

# Function to Get Database Connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'sql12.freesqldatabase.com'),
            user=os.getenv('DB_USER', 'sql12760785'),
            password=os.getenv('DB_PASSWORD', 'WhCQGbQZyJ'),
            database=os.getenv('DB_NAME', 'sql12760785'),
            port=int(os.getenv('DB_PORT', 3306))
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Database Connection Error: {err}")
        return None


# API Route to Retrieve All Projects
@app.route('/projects', methods=['GET'])
def get_projects():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Project")
    projects = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(projects)

# Home Page Route (Handles Form Submission)
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        conn = get_db_connection()
        if conn is None:
            return "Database connection error", 500

        cursor = conn.cursor()
        cursor.execute("INSERT INTO Submission (name, email, message) VALUES (%s, %s, %s)", (name, email, message))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('thank_you'))
    
    category = request.args.get('category', 'all')
    conn = get_db_connection()
    if conn is None:
        return "Database connection error", 500

    cursor = conn.cursor(dictionary=True)

    if category == 'all':
        cursor.execute("SELECT * FROM Project LIMIT 3")
    else:
        cursor.execute("SELECT * FROM Project WHERE section = %s LIMIT 3", (category,))
    
    project_list = cursor.fetchall()
    cursor.close()

    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT section FROM Project")
    sections = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    
    return render_template('index.html', project_list=project_list, sections=sections, selected_category=category)

# Thank You Page Route
@app.route('/thank-you')
def thank_you():
    return 'Thank You. You Will Be Contacted Soon.'

# API Route to Retrieve All Submissions
@app.route('/submissions', methods=['GET'])
def get_submissions():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Submission")
    submissions = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(submissions)

# Run Application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 10000)))
