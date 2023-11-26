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


if __name__ == '__main__':
    app.run(debug = True)