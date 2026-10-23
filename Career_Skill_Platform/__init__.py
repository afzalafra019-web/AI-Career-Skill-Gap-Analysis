from flask import Flask

app = Flask(__name__)
app.secret_key = "change_this_secret_key_for_your_project"

from Career_Skill_Platform.database import init_db
init_db()

from Career_Skill_Platform import views
