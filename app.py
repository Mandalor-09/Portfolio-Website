from flask import Flask, jsonify, request, render_template, url_for, redirect
import mysql.connector
import os

app = Flask(__name__)

# Database Configuration using MySQL Connector
connection = mysql.connector.connect(
    host=os.environ.get('host'),
    user=os.environ.get('user'),
    password=os.environ.get('password'),
    database=os.environ.get('database')
)

# API Route to Retrieve All Projects
@app.route('/projects', methods=['GET'])
def get_projects():
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Project")
    projects = cursor.fetchall()
    cursor.close()
    return jsonify(projects)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Submission (name, email, message) VALUES (%s, %s, %s)", (name, email, message))
        connection.commit()
        cursor.close()
        return redirect(url_for('thank_you'))
    
    category = request.args.get('category', 'all')
    cursor = connection.cursor(dictionary=True)
    
    if category == 'all':
        cursor.execute("SELECT * FROM Project LIMIT 3")
    else:
        cursor.execute("SELECT * FROM Project WHERE section = %s LIMIT 3", (category,))
    
    project_list = cursor.fetchall()
    cursor.close()
    
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT section FROM Project")
    sections = [row[0] for row in cursor.fetchall()]
    cursor.close()
    
    return render_template('index.html', project_list=project_list, sections=sections, selected_category=category)

# Thank You Route (After Form Submission)
@app.route('/thank-you')
def thank_you():
    return 'Thank You. You Will Be Contacted Soon.'

# API Route to Retrieve All Submissions
@app.route('/submissions', methods=['GET'])
def get_submissions():
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Submission")
    submissions = cursor.fetchall()
    cursor.close()
    return jsonify(submissions)

# Run the Application
if __name__ == '__main__':
    app.run(debug=True)
