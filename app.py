from flask import Flask, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
import surveys 

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)

responses = []
sat_survey = surveys.satisfaction_survey

@app.route("/")
def first_request():
    title = sat_survey.title
    instructions = sat_survey.instructions
    return render_template('index.html', title=title, instructions=instructions)

@app.route("/questions/<int:question_number>")
def ask_question(question_number): 
    question = sat_survey.questions[question_number]
    text = question.question
    choices = question.choices
    return render_template('question.html', text=text, choices=choices)


