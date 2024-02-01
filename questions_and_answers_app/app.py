from flask import Flask, render_template, g, request, session, redirect, url_for
from database import get_db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
import os


bcrypt = Bcrypt()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

#class function to call logged in users
def get_current_user():
    user_result = None
   
    if 'user' in session:
        user = session['user']
        db = get_db()
        user_cur = db.execute('select id, name, password, expert, admin from users where name = ?', [user])
        user_result = user_cur.fetchone()
    
    return user_result

#class function of getting all users at once 
def get_all_users():
    db = get_db()
    users_results = None
    users_cur = db.execute('select id, name, expert, admin from users')
    users_results = users_cur.fetchall()
    return users_results


#home route page
@app.route('/')
def index():
    #calls the function to check if the user is in session
    user = get_current_user()

    return render_template('home.html', user=user)


@app.route('/register', methods=['GET', 'POST'])
def register():

    user = get_current_user()

    if request.method == 'POST':
        hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        db = get_db()
        db.execute('INSERT INTO users (name, password, expert, admin) VALUES (?, ?, ?, ?)',
                   [request.form['name'], hashed_password, '0', '0'])
        db.commit()

        session['user'] = request.form['name']

        return redirect(url_for('index'))
    
    return render_template('register.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():

    user = get_current_user()

    if request.method == 'POST':
        db = get_db()

        name = request.form['name']
        password = request.form['password']

        user_cur = db.execute('select id, name, password from users where name = ?', [name])
        user_result = user_cur.fetchone()

        if user_result and bcrypt.check_password_hash(user_result['password'], password):
            session['user'] = user_result['name']
            return redirect(url_for('index'))
        else:
            return '<h1>Login failed. Invalid username or password.</h1>'

        
    return render_template('login.html', user=user)


@app.route('/question')
def question():
    user = get_current_user()
    return render_template('question.html', user=user)


@app.route('/answer/<question_id>', methods=['GET', 'POST'])
def answer(question_id):
    user = get_current_user()
    db = get_db()
    
    if request.method == 'POST':
        return '<h1>Question ID: {}, Answer: {}</h1>'.format(question_id, request.form['answer'])

    question_cur = db.execute('select id, question_text from questions where id = ?', [question_id])
    question = question_cur.fetchone()
    return render_template('answer.html', user=user, question=question)


@app.route('/ask', methods=['GET', 'POST'])
def ask():
    user = get_current_user()
    db = get_db()

    if request.method == 'POST':
        db.execute('insert into questions (question_text, asked_by_id, expert_id) values (?, ?, ?)', [request.form['question'], user['id'], request.form['expert']])
        db.commit()

        return redirect(url_for('index'))
    
 
    expert_cur = db.execute('select id, name from users where expert = 1')
    expert_results = expert_cur.fetchall()

    return render_template('ask.html', user=user, experts=expert_results)


@app.route('/unanswered')
def unanswered():
    user = get_current_user()

    db = get_db()
    question_cur = db.execute('select questions.id, questions.question_text, users.name from questions join users on users.id = questions.asked_by_id where questions.answer_text is null and questions.expert_id = ?', [user['id']])
    questions = question_cur.fetchall()
    return render_template('unanswered.html', user=user, questions=questions)

@app.route('/users')
def users():
    user = get_current_user()
       
    users_results = get_all_users()
 
    return render_template('users.html', user=user, users=users_results)

@app.route('/promote/<user_id>')
def promote(user_id):
    db = get_db()
    db.execute('update users set expert = 1 where id = ?', [user_id])
    db.commit()
    return redirect(url_for('users'))
    
@app.route('/logout')
def logout():
    session.pop('user', None)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True) 