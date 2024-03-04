from flask import Flask
from flask import Flask, render_template, g, request, session, redirect, url_for


from wtforms import StringField, PasswordField, IntegerField, BooleanField, Form, FormField, FieldList, SubmitField, ValidationError
from wtforms.validators import DataRequired, InputRequired, Length, AnyOf
from collections import namedtuple
from flask_bootstrap import Bootstrap


app = Flask(__name__)

import os
app.config['SECRET_KEY'] = os.urandom(24)

bootstrap = Bootstrap(app)
from flask_bcrypt import Bcrypt
bycrypt = Bcrypt()

#home route page
@app.route('/index.html')
def index():
    return render_template('index.html', template_mode='bootstrap4')

#404 route page
@app.route('/404.html')
def error_404():
    return render_template('404.html'), 404

#about route page
@app.route('/about.html')
def about():
    return render_template('about.html')

#contact route page
@app.route('/contact.html')
def contact():
    return render_template('contact.html')

#feature route page
@app.route('/feature.html')
def feature():
    return render_template('feature.html')

#project route page
@app.route('/project.html')
def project():
    return render_template('project.html')

#service route page
@app.route('/service.hml')
def service():
    return render_template('service.html')

#team route page
@app.route('/team.html')
def team():
    return render_template('team.html')

#testimonial route page
@app.route('/testimonial.html')
def testimonial():
    return render_template('testimonial.html')



# Define the route for the video with a parameter video_id
@app.route('/video/<video_id>')
def video(video_id):
    # You can process the video_id here if needed
    # For example, fetch video details from a database based on the video_id
    # Then pass the video details to the template
    return render_template('video.html', video_id=video_id)


if __name__ == '__main__':
    app.run(debug=True)
