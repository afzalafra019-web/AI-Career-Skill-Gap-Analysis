from flask import render_template, request, redirect, url_for, session, flash
from Career_Skill_Platform import app
from Career_Skill_Platform.database import (
    save_student, get_student, save_learning_progress, get_learning_progress
)

CAREER_SKILLS = {
    "Data Analyst": {
        "Excel": ["Spreadsheet Basics", "Formulas and Functions", "Pivot Tables"],
        "SQL": ["SQL Basics", "Filtering and Sorting", "JOINs and Aggregation"],
        "Python": ["Python Fundamentals", "Lists and Dictionaries", "Pandas Basics"],
        "Data Visualization": ["Chart Selection", "Dashboard Design", "Power BI Basics"],
        "Statistics": ["Mean, Median and Mode", "Probability Basics", "Correlation"],
        "Communication": ["Explaining Insights", "Writing a Short Report"]
    },
    "Python Developer": {
        "Python": ["Variables and Data Types", "Conditions and Loops", "Functions", "OOP Basics"],
        "SQL": ["SQL Basics", "CRUD Queries", "JOINs"],
        "Git": ["Git Basics", "Commits and Branches"],
        "APIs": ["HTTP and REST Basics", "Calling an API", "JSON Handling"],
        "Flask": ["Routes and Views", "Templates", "Forms and Validation"]
    },
    "Web Developer": {
        "HTML": ["HTML Document Structure", "Forms and Inputs", "Semantic HTML"],
        "CSS": ["Selectors and Box Model", "Flexbox", "Responsive Design"],
        "JavaScript": ["Variables and Functions", "DOM Basics", "Events"],
        "Python": ["Python Fundamentals", "Functions"],
        "Flask": ["Routes and Views", "Jinja Templates", "Form Handling"],
        "SQL": ["SQL Basics", "CRUD Queries"]
    },
    "AI Engineer": {
        "Python": ["Python Fundamentals", "Functions and Modules", "Working with Data"],
        "Math": ["Linear Algebra Basics", "Probability Basics"],
        "Machine Learning": ["Supervised Learning", "Train/Test Split", "Model Evaluation"],
        "Generative AI": ["LLM Concepts", "Prompt Engineering", "Responsible AI"],
        "APIs": ["HTTP and REST Basics", "API Keys and Environment Variables"]
    },
    "Generative AI Developer": {
        "Python": ["Python Fundamentals", "Functions and Modules"],
        "Generative AI": ["LLM Concepts", "Prompt Engineering", "System Instructions"],
        "APIs": ["HTTP and REST Basics", "Calling an AI API Safely"],
        "RAG": ["Embeddings Overview", "Retrieval Pipeline", "Grounded Responses"],
        "Databases": ["SQL Basics", "Storing and Retrieving Records"]
    }
}

STUDY_CONTENT = {
    "Python": {
        "Python Fundamentals": ("Python is a programming language. Values have types such as int, float, str and bool. Use variables to store values.", "name = 'Afra'\\nprint(name)\\n# Output: Afra", ["Create variables for your name and age.", "Print the result of 5 + 7."]),
        "Variables and Data Types": ("Variables are names that refer to values. Common types include strings, integers, floats and booleans.", "age = 23\\nstudent = True", ["Create one variable of each type.", "Use type() to inspect a variable."]),
        "Conditions and Loops": ("if/elif/else makes decisions. for and while loops repeat instructions.", "for number in range(1, 4):\\n    print(number)", ["Print numbers 1 to 10.", "Write an if statement checking whether a number is positive."]),
        "Functions": ("A function is a reusable block of code defined with def. Parameters receive input and return sends a result back.", "def add(a, b):\\n    return a + b\\nprint(add(2, 3))", ["Write a function that squares a number.", "Write a function that greets a name."]),
        "OOP Basics": ("Object-oriented programming organizes code into classes and objects. A class defines attributes and behavior.", "class Student:\\n    def __init__(self, name):\\n        self.name = name", ["Create a Book class with a title.", "Explain the purpose of __init__."])
    },
    "SQL": {
        "SQL Basics": ("SQL is used to query relational databases. SELECT reads columns from a table.", "SELECT name, email FROM students;", ["Write a query selecting all columns from students.", "Select only the email column."]),
        "Filtering and Sorting": ("WHERE filters rows. ORDER BY sorts results.", "SELECT * FROM students WHERE career = 'Data Analyst' ORDER BY name;", ["Filter students by a chosen career.", "Sort results by email."]),
        "JOINs and Aggregation": ("JOIN combines related tables. GROUP BY creates groups; COUNT, SUM and AVG calculate summaries.", "SELECT career, COUNT(*) FROM students GROUP BY career;", ["Count records by career.", "Describe when an INNER JOIN is useful."]),
        "CRUD Queries": ("CRUD means Create, Read, Update and Delete. SQL uses INSERT, SELECT, UPDATE and DELETE.", "INSERT INTO tasks (title) VALUES ('Learn SQL');", ["Write a SELECT query.", "Write an UPDATE statement with a WHERE condition."]),
        "JOINs": ("A JOIN combines rows using related columns.", "SELECT students.name, progress.topic FROM students JOIN progress ON students.email = progress.email;", ["Describe a primary key.", "Explain why JOIN conditions matter."])
    },
    "Excel": {
        "Spreadsheet Basics": ("A spreadsheet stores data in cells arranged by rows and columns. Use clear headings and consistent formats.", "Enter Name in A1 and Score in B1.", ["Create a table with five students.", "Format the heading row."]),
        "Formulas and Functions": ("Formulas begin with =. Common functions include SUM, AVERAGE, COUNTIF and IF.", "=AVERAGE(B2:B10)", ["Calculate a total with SUM.", "Use AVERAGE on five numbers."]),
        "Pivot Tables": ("Pivot tables summarize large tables by categories, such as total sales by region.", "Select data → Insert → PivotTable.", ["Make a count by category.", "Summarize values by month."])
    },
    "HTML": {
        "HTML Document Structure": ("HTML describes the structure of a web page using elements such as headings, paragraphs, links and forms.", "<h1>My Page</h1>\\n<p>Hello world.</p>", ["Create a page with a heading and paragraph.", "Add a link."]),
        "Forms and Inputs": ("Forms collect user input. Labels improve accessibility; input names are submitted to the server.", "<label>Email <input type='email' name='email'></label>", ["Create a form with name and email fields.", "Add a submit button."]),
        "Semantic HTML": ("Semantic elements describe purpose, such as header, nav, main, section and footer.", "<main><section><h2>About</h2></section></main>", ["Build a page with header, main and footer.", "Explain why semantic HTML helps."])
    },
    "CSS": {
        "Selectors and Box Model": ("CSS styles HTML. The box model includes content, padding, border and margin.", "p { margin: 1rem; padding: .5rem; }", ["Style all headings.", "Add padding to a card."]),
        "Flexbox": ("Flexbox aligns and distributes items in a container.", ".row { display: flex; gap: 1rem; }", ["Place two cards side by side.", "Center an item with Flexbox."]),
        "Responsive Design": ("Responsive design adapts layouts to different screen sizes using flexible dimensions and media queries.", "@media (max-width: 600px) { .row { flex-direction: column; } }", ["Add a mobile media query.", "Test a page at narrow width."])
    },
    "JavaScript": {
        "Variables and Functions": ("JavaScript adds behavior to web pages. Use const for values that are not reassigned and function declarations for reusable logic.", "const greet = name => `Hello ${name}`;", ["Write a function to add two numbers.", "Create a const variable."]),
        "DOM Basics": ("The DOM represents a web page as objects. JavaScript can find and update elements.", "document.querySelector('h1').textContent = 'Welcome';", ["Change a paragraph using JavaScript.", "Select an element by ID."]),
        "Events": ("Events such as click and submit let a page respond to user actions.", "button.addEventListener('click', () => alert('Hello'));", ["Add a click event.", "Prevent a form's default submit behavior."])
    }
}

def parse_skills(raw):
    return [item.strip() for item in raw.replace(";", ",").split(",") if item.strip()]

def level_map(raw):
    result = {}
    for item in raw.split(","):
        if ":" in item:
            skill, level = item.split(":", 1)
            result[skill.strip()] = level.strip().lower()
    return result

def get_topic_material(skill, topic):
    content = STUDY_CONTENT.get(skill, {}).get(topic)
    if content:
        explanation, example, exercises = content
    else:
        explanation = f"This topic builds your understanding of {topic} as part of the {skill} skill. Read an introductory guide, practise with a small example, and write down what you learned."
        example = f"Practice task: create a small example that demonstrates {topic}."
        exercises = [f"Write a short explanation of {topic}.", f"Build a small practice task using {topic}."]
    return {"explanation": explanation, "example": example, "exercises": exercises}

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    existing = None
    email = session.get("email")
    if email:
        existing = get_student(email)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        education = request.form.get("education", "").strip()
        career = request.form.get("career", "").strip()
        known_skills = request.form.get("known_skills", "").strip()
        skill_levels = request.form.get("skill_levels", "").strip()

        if not name or not email:
            flash("Please enter your name and email.", "error")
            return render_template("profile.html", student=request.form)

        save_student(name, email, education, career, known_skills, skill_levels)
        session["email"] = email
        session["name"] = name
        session["career"] = career
        flash("Your profile has been saved.", "success")
        return redirect(url_for("career"))

    return render_template("profile.html", student=existing or {})

@app.route("/career", methods=["GET", "POST"])
def career():
    selected = session.get("career", "")
    if request.method == "POST":
        selected = request.form.get("career", "").strip()
        if selected not in CAREER_SKILLS:
            flash("Please choose one of the listed careers.", "error")
            return render_template("career.html", careers=CAREER_SKILLS.keys(), selected_career=selected)
        session["career"] = selected
        email = session.get("email")
        if email:
            student = get_student(email)
            if student:
                save_student(student["name"], email, student["education"], selected, student["known_skills"], student["skill_levels"])
        return redirect(url_for("skill_gap"))
    return render_template("career.html", careers=CAREER_SKILLS.keys(), selected_career=selected)

@app.route("/skill-gap", methods=["GET", "POST"])
def skill_gap():
    career_name = session.get("career", "")
    if career_name not in CAREER_SKILLS:
        flash("Choose your career first.", "error")
        return redirect(url_for("career"))
    email = session.get("email")
    student = get_student(email) if email else None
    raw_known = (student or {}).get("known_skills", "")
    raw_levels = (student or {}).get("skill_levels", "")
    known = parse_skills(raw_known)
    levels = level_map(raw_levels)
    requirements = CAREER_SKILLS[career_name]
    analyzed = request.method == "POST" or bool(known or levels)
    if request.method == "POST":
        raw_known = request.form.get("known_skills", raw_known).strip()
        raw_levels = request.form.get("skill_levels", raw_levels).strip()
        known = parse_skills(raw_known)
        levels = level_map(raw_levels)
        if email and student:
            save_student(student["name"], email, student["education"], career_name, raw_known, raw_levels)
    missing = [skill for skill in requirements if skill.lower() not in [s.lower() for s in known]]
    gap_skills = []
    for skill in requirements:
        level = levels.get(skill, "beginner")
        if skill not in known or level in ("beginner", "basic", "none", "0"):
            gap_skills.append(skill)
    return render_template(
        "skill_gap.html",
        career=career_name,
        requirements=requirements,
        analyzed=analyzed,
        known_skills=known,
        skill_levels=levels,
        missing_skills=missing,
        gap_skills=gap_skills,
        raw_known=raw_known,
        raw_levels=raw_levels
    )

@app.route("/learning-plan")
def learning_plan():
    career_name = session.get("career", "")
    if career_name not in CAREER_SKILLS:
        flash("Choose your career first.", "error")
        return redirect(url_for("career"))
    email = session.get("email", "")
    student = get_student(email) if email else None
    known = parse_skills((student or {}).get("known_skills", ""))
    levels = level_map((student or {}).get("skill_levels", ""))
    progress = get_learning_progress(email) if email else []
    completed_keys = {(p["skill"], p["topic"]): bool(p["completed"]) for p in progress}
    plan = []
    for skill, topics in CAREER_SKILLS[career_name].items():
        level = levels.get(skill, "beginner")
        if skill in known and level in ("intermediate", "advanced", "proficient"):
            continue
        for topic in topics:
            plan.append({
                "skill": skill,
                "topic": topic,
                "study_url": url_for("study_material", skill=skill, topic=topic),
                "completed": completed_keys.get((skill, topic), False)
            })
    total = len(plan)
    completed = sum(1 for item in plan if item["completed"])
    percentage = round(completed * 100 / total) if total else 0
    return render_template(
        "learning_plan.html",
        learning_plan=plan,
        progress=progress,
        email=email,
        total_topics=total,
        completed_topics=completed,
        progress_percentage=percentage
    )

@app.route("/progress", methods=["POST"])
def update_progress():
    email = session.get("email")
    if not email:
        flash("Save your profile before tracking progress.", "error")
        return redirect(url_for("profile"))
    skill = request.form.get("skill", "").strip()
    topic = request.form.get("topic", "").strip()
    completed = request.form.get("completed") == "1"
    save_learning_progress(email, skill, topic, completed)
    flash("Learning progress updated.", "success")
    return redirect(url_for("learning_plan"))

@app.route("/study-material")
def study_material():
    skill = request.args.get("skill", "").strip()
    topic = request.args.get("topic", "").strip()
    career_name = session.get("career", "")
    allowed = CAREER_SKILLS.get(career_name, {})
    if skill not in allowed or topic not in allowed[skill]:
        flash("Please choose a topic from your learning plan.", "error")
        return redirect(url_for("learning_plan"))
    material = get_topic_material(skill, topic)
    external_links = [
        {"name": f"Search learning resources for {topic}", "url": "https://www.google.com/search?q=" + topic.replace(" ", "+") + "+" + skill.replace(" ", "+")},
        {"name": f"Official documentation for {skill}", "url": {
            "Python": "https://docs.python.org/3/tutorial/",
            "SQL": "https://www.w3schools.com/sql/",
            "HTML": "https://developer.mozilla.org/en-US/docs/Web/HTML",
            "CSS": "https://developer.mozilla.org/en-US/docs/Web/CSS",
            "JavaScript": "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
            "Flask": "https://flask.palletsprojects.com/",
            "Excel": "https://support.microsoft.com/excel"
        }.get(skill, "https://developer.mozilla.org/")}
    ]
    return render_template("study_material.html", skill=skill, topic=topic, material=material, external_links=external_links)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        flash("Thank you! Your message has been received.", "success")
        return redirect(url_for("contact"))
    return render_template("contact.html")
