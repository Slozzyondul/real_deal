from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
#from werkzeug.security import generate_password_hash
from flask_admin.contrib.fileadmin import FileAdmin
from os.path import dirname, join
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/solo/Desktop/Flask_framework/flask_admin/admin_db.db'
app.config['SECRET_KEY'] = 'mykey'

db = SQLAlchemy(app)
admin = Admin(app, template_mode='bootstrap4')
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return Users1.query.filter_by(id=int(user_id)).first()

class Users1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(50))
    age = db.Column(db.Integer)
    birthday = db.Column(db.DateTime)
    comments = db.relationship('Comment', backref='users1', lazy='dynamic')

    def __repr__(self):
        return '<Users1 %r>' % (self.username)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users1.id'))

    def __repr__(self):
        return '<Comment %r>' % (self.username)

#hiding the password column from users and modifying other entries for the admin  
class UserView(ModelView, UserMixin):
    column_exclude_list = ['age']
    column_display_pk = True
    can_create = True
    can_edit = True
    can_delete = True
    can_export = True
    #pop up window to register new user
    create_modal = True

    #def on_model_change(self, form, model, is_created):
        #model.password = generate_password_hash(model.password, method='sha256')
    
    #inline_models = [Comment] 

    #authontication for views
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        return '<h1>You arent in yet!</>'

class CommentView(ModelView):
    create_modal = True
    can_export = True

class NotificationsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/notification.html')
    
    
    
admin.add_view(UserView(Users1, db.session))
admin.add_view(CommentView(Comment, db.session))

#adding upload option
path = join(dirname(__file__), 'uploads')
admin.add_view(FileAdmin(path, '/uploads/', name='Uploads'))

#adding notification view class
admin.add_view(NotificationsView(name="Notifications", endpoint="notify"))

@app.route('/login')
def login():
    user = Users1.query.filter_by(id=1).first()
    login_user(user)
    return redirect(url_for('admin.index'))

@app.route('/logout')
def logout_user ():
    return redirect (url_for('admin.index'))


if __name__ == '__main__':
    app.run(debug=True)