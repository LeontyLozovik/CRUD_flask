from flask import Flask, redirect, request, render_template, session, url_for
import os
from models import db, Quiz, Question, User, db_add_new_data
from random import shuffle

BASE_DIR = os.getcwd()
DB_PATH = os.path.join(BASE_DIR, 'db', 'db_quiz.db')

app = Flask(__name__,
            static_folder=os.path.join(BASE_DIR, 'static'),
            template_folder=os.path.join(BASE_DIR, 'templates'))

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SECRET_KEY'] = 'very_secret_secret_key'

db.init_app(app)

with app.app_context():
    db_add_new_data()


@app.route('/')
def index():
    #question = Question('1', '1', '2', '3', '4')
    question = None
    return render_template('update_question.html', question=question)


# @app.route('/', methods=['POST', 'GET'])
# def index():
#     if request.method == 'GET':
#         quizzes = Quiz.query.all()
#         return render_template('start.html', quizzes=quizzes)
#     else:
#         session['quiz_id'] = request.form.get('quiz')
#         session['question_number'] = 0
#         return redirect(url_for('questions'))


@app.route('/admin/', methods=['POST', 'GET'])
def admin():
    if request.method == 'GET':
        list_of_questions = Question.query.all()
        return render_template('admin.html', list_of_questions=list_of_questions)
    elif request.method == 'POST':
        quest = request.form.get('question')
        answer = request.form.get('answer')
        wrong1 = request.form.get('wrong1')
        wrong2 = request.form.get('wrong2')
        wrong3 = request.form.get('wrong3')
        question = Question(quest, answer, wrong1, wrong2, wrong3)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('admin'))
    elif request.method == 'PUT':
        question = Question.query.filter_by(id=new_question.id).first()
        question.question = new_question.question
        question.answer = new_question.answer
        question.wrong1 = new_question.wrong1
        question.wrong2 = new_question.wrong2
        question.wrong3 = new_question.wrong3
        db.session.commit()
        return redirect(url_for('admin'))
    else:
        return "404"


@app.route('/admin/delete/<int:id>')
def delete_question(id):
    question = Question.query.filter_by(id=id).first()
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('admin'))


@app.route('/admin/update/<int:question_id>', methods=['POST', 'GET'])
def update_question(question_id):
    if request.method == 'GET':
        question = Question.query.filter_by(id=question_id).first()
        return render_template('update_question.html', question=question)
    elif request.method == 'POST':
        question = Question.query.filter_by(id=question_id).first()
        question.question = request.form.get('question')
        question.answer = request.form.get('answer')
        question.wrong1 = request.form.get('wrong1')
        question.wrong2 = request.form.get('wrong2')
        question.wrong3 = request.form.get('wrong3')
        db.session.commit()
        return redirect(url_for('admin'))
    else:
        return "404"


@app.route('/question/', methods=['POST', 'GET'])
def questions():
    if not session['quiz_id'] or session['quiz_id'] == -1:
        return redirect(url_for('index'))

    quiz = Quiz.query.filter_by(id=session['quiz_id']).all()
    if int(session['question_number']) >= len(quiz[0].question):
        return redirect(url_for('result'))
    else:
        question = quiz[0].question[session['question_number']]
        answers = [question.answer, question.wrong1, question.wrong2, question.wrong3]
        shuffle(answers)
        return render_template('question.html', question=question.question, answers=answers)


app.run(debug=True)
