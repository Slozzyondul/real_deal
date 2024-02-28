from flask import Flask, render_template, request, session, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user, fresh_login_required
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import urlparse, urljoin
from datetime import timedelta
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisasecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
app.config['USE_SESSION_FOR_NEXT'] = True
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=20)
app.config['TIME_TO_EXPIRE'] = 3600

login_manager = LoginManager(app)
#auto redirecting the user to the login screen  
login_manager.login_view = 'login'
login_manager.login_message = 'You can\'t access that page. You need to login first.'
login_manager.refresh_view = 'login'
login_manager.needs_refresh_message = 'You need to login again!'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

serializer = URLSafeTimedSerializer(app.secret_key)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))

    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    session_token = db.Column(db.String(100), unique=True)

    def get_id(self):
        return (self.session_token)

@login_manager.user_loader
def load_user(session_token):
    user = User.query.filter_by(session_token=session_token).first()
    try:
        serializer.loads(session_token, max_age=60)
    except SignatureExpired:
        user.session_token = None    
        db.session.commit()
        return None
    
    return user

def create_user():
    user = User(username='solo', password='solo', session_token=serializer.dumps(['solo', 'solo']))
    db.session.add(user)
    db.session.commit()

def update_token():
    solo = User.query.filter_by(username='solo').first()
    login_user(solo, remeber=True)
    return 'you are logged in'    


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if not user:
            return 'User does not exist in the database!'
        

        login_user(user, remember=True)

        if 'next' in session: 
            next = session['next']

            if is_safe_url(next) and next is not None:
                return redirect(next)


        return '<h1>You are now logged in</h1>'
    
    session['next'] = request.args.get('next')
    return render_template('login.html')

@app.route('/') 

def index():
    user = User.query.filter_by(username='solo').first()
    
    session_token = serializer.dumps(['solo', 'solo'])
    user.session_token = session_token
    db.session.commit()

    login_user(user, remember=True)
    return 'You are now logged in!'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return '<h1>You are logged out!</h1>'

@app.route('/fresh')
@fresh_login_required
def fresh():
    return '<h1>You have a fresh session!</h1>'

if __name__ == '__main__':
    app.run(debug=True)
