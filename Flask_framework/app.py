from flask import Flask, render_template  
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, IntegerField, BooleanField, Form, FormField, FieldList, SubmitField, ValidationError
from wtforms.validators import DataRequired, InputRequired, Length, AnyOf
from collections import namedtuple
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Mysecret!'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LewPngpAAAAADo3YJk-4OobI9hXvhDok4eDUdKZ'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LewPngpAAAAAE7Pzhi03OqEgb0xQ0nMSjRqpEi2'
#temporarily deactivate recapture during development stage
app.config['TESTING'] = True

bootstrap = Bootstrap(app)

class TelephoneForm(Form):
    country_code = IntegerField('country code') 
    area_code = IntegerField('area code')
    number = StringField('number')    

class YearForm(Form):
    year = IntegerField('year')
    total = IntegerField('total') 


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired('A username is a MUST!'), Length(min=4, max=20, message='Must be between 4 and 20 characters')])
    password = PasswordField('password', validators=[InputRequired('A password is a MUST!'), AnyOf(values=['solo', 'secret', 'password'])])
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')
    age = IntegerField('age')
    true = BooleanField('true')
    email = StringField('email')
    home_phone = FormField(TelephoneForm)
    mobile_phone = FormField(TelephoneForm)
    years = FieldList(FormField(YearForm))

class NameForm(LoginForm):
    first_name = StringField('first name')
    last_name = StringField('last name')

class User:
    def __init__(self, username, age, email):
        self.username = username
        self.age = age
        self.email = email

    #inline validation
    def validate_username(form, field):
        if field.data != 'solomononondula@gmail.com':
            raise ValidationError('Try again')
            

@app.route('/', methods=['GET', 'POST'])
def index():
    myuser = User('Solomon', 27, 'solomon@ondula.com')
    
    group = namedtuple('Group', ['year', 'total'])
    g1 = group(2005, 1000)
    g2 = group(2006, 1500)
    g3 = group(2007, 1700)

    years = {'years' : [g1, g2, g3]}

    form = NameForm(obj=myuser, data=years)

    #deleting the mobile phone column
    del form.mobile_phone

    if form.validate_on_submit():
        #return '<h1>Username: {} Password: {}<h1>'.format(form.username.data, form.password.data)
        #return '<h1> Country code: {}, Area code: {}, Number: {}'.format(form.home_phone.countr_code.data)
         
        output = '<h1>'

        for f in form.years:
             output += 'Year: {}'.format(f.year.data)
             output += 'Total: {} <br>'.format(f.total.data)

        output += '</h1>'

        return output     
 
    return render_template('index.html', form=form)

@app.route('/dynamic', methods=['GET', 'POST'])
def dynamic():
    class DynamicForm(FlaskForm):
        pass

    DynamicForm.name = StringField('name')

    names = ['middle_name', 'last_name', 'nickname', 'maiden_name']

    for name in names:
        setattr(DynamicForm, name, StringField(name))

    form = DynamicForm()
 
    if form.validate_on_submit():
        return 'Form has been validated. Name: {}'.format(form.name.data)

    return render_template('dynamic.html', form=form, names=names)

@app.route('/form', methods=['GET', 'POST'])
def form():
    form = LoginForm()

    if form.validate_on_submit():
        return '<h1> The  username is {}. The password is {}.</h1>'.format(form.username.data, form.password.data)
    return render_template('form.html', form=form)

@app.route('/index_bootstrap', methods=['GET', 'POST'])
def index_bootstrap():
    form = LoginForm()
    if form.validate_on_submit():
        return 'Form successfully Submitted!'
    return render_template('index_bootstrap.html', form=form)

if __name__ == '__main__':
    app.run(debug=True) 