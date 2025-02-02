from flask import Flask, jsonify, request ,render_template ,url_for ,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Project Model
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(200), unique=True, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    tech_used = db.Column(db.String(300), nullable=False)
    github = db.Column(db.String(300), nullable=True)
    demo = db.Column(db.String(300), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

# Define the Submission Model (Frontend Form Data)
class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Submission('{self.name}', '{self.email}')"

# Function to create the database
def create_database():
    with app.app_context():
        db.create_all()
        print("Database created successfully!")

# Function to insert projects while avoiding duplicates
def insert_projects():
    with app.app_context():
        create_database()

        existing_project_names = {project.name for project in Project.query.all()}

        projects = [
            Project(
                section="Full-Stack Web Application", 
                name="Instagram Clone Full-Stack Web Application", 
                desc="Built an Instagram clone with user authentication, profile management, and post creation. Features include following/unfollowing, liking posts, live chat, and public/private account settings. Implemented responsive design and real-time interactions with Django and front-end technologies.", 
                tech_used="Django, HTML, CSS, JavaScript, SQLite", 
                github="https://github.com/Mandalor-09/Instagram-Clone-using-django/tree/master/InstaClone",  
                demo="https://your-demo-link.com"
            ),
            Project(
                section="AI", 
                name="AI-Powered Study Plan Generator", 
                desc="Developed an AI-driven study plan generator using Gemini technology to personalize study schedules, source relevant blogs, and curate YouTube content. Implemented RAG features for interactive learning, linking resources seamlessly, and enabling user interaction for doubts and tests.", 
                tech_used="Langchain, CrewAI, Streamlit", 
                github="https://github.com/Mandalor-09/LearnMate-AI",  
                demo="https://your-demo-link.com"
            ),
            Project(
                section="AI", 
                name="Resume to Video (LLama 3 Technology)", 
                desc="Created an application that transforms resumes into professional summary videos using LICA and Groq (LLama 3) APIs. Successfully deployed the application, demonstrating expertise in building user-friendly tools.", 
                tech_used="LLama 3, LICA, Groq", 
                github="https://huggingface.co/spaces/nimo007/VoiceMyResume",  
                demo="https://your-demo-link.com"
            ),
            Project(
                section="AI", 
                name="Diet Recommendation App (Gemini Technology)", 
                desc="Developed a RAG system for personalized diet plans, enhancing user fitness goals. Utilized Gemini technology for tailored diet suggestions, contributing to user well-being.", 
                tech_used="Gemini Technology", 
                github="https://github.com/Mandalor-09/Diet-Recommendation-App",  
                demo="https://mi-vyre.onrender.com/",
                is_active=True
            ),
            Project(
                section="AI", 
                name="Chatbot", 
                desc="Fine-tuned the Llama 3 language model to create a chatbot capable of negotiating prices in a simulated environment. Demonstrated proficiency in large language model training, conversational AI development, and data collection and preparation.", 
                tech_used="Llama 3", 
                github="https://github.com/Mandalor-09/Bg_Bot",  
                demo="https://your-demo-link.com"
            ),
            Project(
                section="Machine Learning", 
                name="Phishing Threat Detection Model", 
                desc="Built a machine learning model for real-time phishing threat detection, achieving 95% accuracy using logistic regression and random forest. Successfully deployed the model into a web application for immediate threat identification, showcasing expertise in developing and deploying machine learning models.", 
                tech_used="Machine Learning, NLP, Logistic Regression, Random Forest", 
                github="https://github.com/Mandalor-09/Phishing",  
                demo="https://your-demo-link.com"
            ),
            Project(
                section="AI", 
                name="Submission Evaluation System", 
                desc="Developed an AI-powered submission evaluation system that automatically checks coding assignment submissions, compares them against test cases, and provides real-time feedback. Implemented a grading system that evaluates code efficiency, accuracy, and completeness.", 
                tech_used="Python, FastAPI, LangChain, OpenAI API", 
                github="https://github.com/Mandalor-09/Submission-Evaluation-System",  
                demo="https://your-demo-link.com"
            )
        ]

        # Filter out projects that are already in the database
        new_projects = [project for project in projects if project.name not in existing_project_names]

        if new_projects:
            db.session.bulk_save_objects(new_projects)
            db.session.commit()
            print(f"{len(new_projects)} projects added successfully!")
        else:
            print("No new projects to add. All are already in the database.")

# API Route to Retrieve All Projects
@app.route('/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([
        {
            "section": project.section,
            "name": project.name,
            "desc": project.desc,
            "tech_used": project.tech_used,
            "github": project.github,
            "demo": project.demo,
            "is_active": project.is_active
        } for project in projects
    ])

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        new_submission = Submission(name=name, email=email, message=message)
        db.session.add(new_submission)
        db.session.commit()
        return redirect(url_for('thank_you'))

    # Get selected category from frontend (default: 'all')
    category = request.args.get('category', 'all')

    # Fetch projects based on category
    if category == 'all':
        project_list = Project.query.limit(3).all()  # Show only 3 projects
    else:
        project_list = Project.query.filter_by(section=category).limit(3).all()

    # Get unique sections for filtering
    sections = list(set([project.section for project in Project.query.all()]))

    return render_template('index.html', project_list=project_list, sections=sections, selected_category=category)


# Thank You Route (After Form Submission)
@app.route('/thank-you')
def thank_you():
    return 'Thank You. You Will Be Contacted Soon.'

# API Route to Retrieve All Submissions
@app.route('/submissions', methods=['GET'])
def get_submissions():
    submissions = Submission.query.all()
    return jsonify([
        {
            "id": submission.id,
            "name": submission.name,
            "email": submission.email,
            "message": submission.message
        } for submission in submissions
    ])

# Run the Application
if __name__ == '__main__':
    insert_projects()
    app.run(debug=True)
