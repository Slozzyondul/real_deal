from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['TESTING'] = False

app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = None
app.config['MAIL_PASSWORD'] = None
app.config['MAIL_DEFAULT_SENDER'] = None
app.config['NAIL_MAX_EMAILS'] = None
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)

@app.route('/')
def index():
    msg = Message('Hi there, Solo here!',
           recipients=['solomonondula@gmail.com', 'solomonondula472@gmail.com'])
    #msg.add_recipient('solomononula@students.uonbi.ac.ke')
    #msg.body = 'Here is the body!'
    msg.html = '<b>This is a test email sent from Solo\'s app. You don\'t have to reply.</b>'

    #attaching a file
    with app.open_resource('sol.jpg') as solo:
        msg.attach('solo.jpg', 'image/jpg', solo.read())
        

    mail.send(msg)
 
    return 'Message has been sent'

@app.route('/bulk')
def bulk():
    users = [{'name' : 'Solomon', 'email' : 'solomonondula@gmail.com'}]

    with mail.connect() as conn:
        for user in users:
            msg = Message('Bulk!', recipients=[user['email']])
            msg.body = 'Hey There!'
            conn.send(msg)

        
if __name__ == '__main__':
    app.run()
