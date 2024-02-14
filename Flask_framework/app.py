from flask import Flask, render_template  
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField
from wtforms.validators import DataRequired, InputRequired, Length, AnyOf

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Mysecret!'

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired('A username is a MUST!'), Length(min=4, max=20, message='Must be between 4 and 20 characters')])
    password = PasswordField('password', validators=[InputRequired('A password is a MUST!')])
    age = IntegerField('age')
    true = BooleanField('true')
    email = StringField('email')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()

    if form.validate_on_submit():
        return '<h1>Username: {} Password: {}<h1>'.format(form.username.data, form.password.data)
    
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True) 