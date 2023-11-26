from pprint import pprint
from flask import Flask, render_template, request, flash, redirect, session
from model import Database
app = Flask(__name__)
app.secret_key = '@#$123456&*()'
db = Database()

@app.route('/')
def index():
    return redirect('/question_list')

@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        data = request.form.to_dict()
        # data looks like this
        # {'0': 'choice 1',
        # '1': 'choice 2',
        # 'choice': '1',
        # 'question': 'this is question'}
        question = data.pop('question')
        correct_choice_idx = data.pop('choice')

        choices = []
        
        for k, v in data.items():
            choices.append([v, 'Y'] if k == correct_choice_idx else [v, 'N'])
        # choices looks like this
        # [['choice 1', 'N'], ['choice 2', 'Y'], ...]
        
        if db.insert_question(question, choices):
            flash('success', 'Successfully added question!')
        else:
            flash('danger', 'Failed to add question!')

        return redirect('/question_list')

    return render_template('add_question.html', title='Add Question')

@app.route('/question_list/')
def question_list():
    data = db.read_question(None)
    return render_template('question_list.html', data=data, title="Question List")

@app.route('/edit_question/<int:question_id>', methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == 'POST':
        data = request.form.to_dict()
        # data looks like this
        # {'0': 'choice 1',
        # '1': 'choice 2',
        # 'choice': '1',
        # 'question': 'this is question'}
        question = data.pop('question')
        correct_choice_idx = data.pop('choice')

        choices = []
        
        for k, v in data.items():
            choices.append([v, 'Y'] if k == correct_choice_idx else [v, 'N'])
        # choices looks like this
        # [['choice 1', 'N'], ['choice 2', 'Y'], ...]
        
        if db.edit_question(question_id, question, choices):
            flash('success', 'Successfully edited question!')
        else:
            flash('danger', 'Failed to edit question')
        return redirect('/question_list')

    question = db.read_question(question_id)
    return render_template('edit_question.html', data=question[0], title='Edit Question')

@app.route('/delete_question/<int:question_id>')
def delete_question(question_id):
    if db.delete_question(question_id):
        flash('success', 'Successfully deleted question!')
    else:
        flash('danger', 'Failed to delete question!')
    return redirect('/question_list')

questions = None  # storing questions from database
question_number = 0 
correct = 0 # number of correctly answered questions
wrong = 0   # number of incorrectly answered questions

@app.route('/start_quiz')
def start_quiz():
    global questions
    global question_number
    global correct
    global wrong

    question_number = 0
    correct = 0
    wrong = 0

    questions = db.read_question(None)

    if (len(questions) == 0):
        questions_exist = False
    else:
        questions_exist = True

    return render_template('start_quiz.html', title='Quiz', questions_exist=questions_exist)

@app.route('/answer_quiz')
def answer_quiz():
    question = questions[question_number]

    return render_template('answer_quiz.html', question_number=question_number+1, question=question, title='Quiz')

@app.route('/process_answer', methods=["POST", "GET"])
def process_answer():
    global question_number
    global correct
    global wrong

    if request.method == "POST":
        if questions[question_number][2][int(request.form['choice'])][2] == 'Y':
            correct += 1
            print('correct')
        else:
            wrong += 1
            print('wrong')
        question_number += 1
    
        if question_number >= len(questions):
            return redirect('/show_score')

    return redirect('/answer_quiz')

@app.route('/show_score')
def show_score():
    return render_template('show_score.html', title='Quiz', correct=correct, wrong=wrong)

if __name__ == '__main__':
    app.run(debug = True)