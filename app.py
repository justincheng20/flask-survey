from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)

sat_survey = surveys.satisfaction_survey


@app.route("/")
def first_request():
    title = sat_survey.title
    instructions = sat_survey.instructions
    return render_template(
                            'index.html', title=title,
                            instructions=instructions)


@app.route("/", methods=['POST'])
def init_answers():
    session['responses'] = []
    return redirect("/question/0")


@app.route("/question/<int:question_number>", methods=['GET', 'POST'])
def ask_question(question_number):

    # answers = session['responses']
    # Tried to refactor this but it broke the code. WHY?

    if request.method == 'POST':
        f = request.form.to_dict()
        if len(f.keys()) > 0:
            for key in f.keys():
                answer_to_previous = key
            responses = session['responses']
            responses.append(answer_to_previous)
            session['responses'] = responses
        print(session)
        print(session['responses'])

    if len(session['responses']) != question_number:
        flash("Redirected to correct question!")
        return redirect(f"/question/{len(session['responses'])}")

    if question_number < len(sat_survey.questions):
        question = sat_survey.questions[question_number]
        question_number += 1
        text = question.question
        choices = question.choices
    else:
        return redirect("/thanks")

    return render_template(
                            'question.html', text=text, choices=choices,
                            question_number=question_number)


# @app.route("/question/<int:question_number>", methods=['POST'])
# def ask_question(question_number):

#     f = request.form.to_dict()
#     if len(f.keys()) > 0:
#         for key in f.keys():
#             answer_to_previous = key
#         responses.append(answer_to_previous)
#     print(responses)

#     if len(responses) != question_number:
#         flash("Incorrect question! Redirected.")
#         return redirect(f"/question/{len(responses)}")

    # if question_number < len(sat_survey.questions):
    #     question = sat_survey.questions[question_number]
    #     question_number += 1
    #     text = question.question
    #     choices = question.choices
    # else:
    #     return redirect("/thanks")

#     return render_template(
#         'question.html', text=text, choices=choices,
#         question_number=question_number)


@app.route("/thanks")
def say_thanks():
    return render_template("thank_you.html")
