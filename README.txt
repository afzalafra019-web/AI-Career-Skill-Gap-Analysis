AI-Assisted Career Skill Gap Analysis and Personalized Learning System
====================================================================

SETUP
1. Extract this ZIP file.
2. Open the extracted folder "Career_Skill_Platform_Complete" in Visual Studio Code.
3. Open Terminal (Ctrl+Shift+P, type "Terminal: Create New Terminal").
4. Run:
   python -m pip install -r requirements.txt
5. Run:
   python runserver.py
6. Open the address printed in the terminal, usually http://127.0.0.1:5000

PROJECT STRUCTURE
runserver.py
requirements.txt
Career_Skill_Platform/
    __init__.py
    database.py
    views.py
    templates/
        layout.html
        index.html
        profile.html
        career.html
        skill_gap.html
        learning_plan.html
        study_material.html
        about.html
        contact.html

IMPORTANT
- This is a clean, consistent replacement project. Keep a backup of your existing project before replacing files.
- The application uses SQLite and creates career_skill_platform.db automatically.
- The learning resources and study notes are starter learning content, not a replacement for official course materials.
