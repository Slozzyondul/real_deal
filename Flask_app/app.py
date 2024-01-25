from flask import Flask, jsonify, request, url_for, redirect, session, render_template, g
import sqlite3

app = Flask(__name__)

app.config['DEBUG'] = True

app.config['SECRET_KEY'] = 'secret!'

def connect_db():
    sql = sqlite3.connect('/home/solo/Desktop/Flask_app/data.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite_db = connect_db()
    return g.sqlite_db    

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
        

@app.route('/')
def index():
    session.pop('name', None)
    return '<h1>Welcome To Solomon Ondula Page!</h1>'

@app.route('/home', methods=['POST', 'GET'], defaults={'name': 'Jesus_Christ'})
@app.route('/home/<string:name>', methods=['POST', 'GET'])
def home(name): 
    session['name'] = name
    #displaying database in the home page 
    db = get_db()
    cur = db.execute('select id, name, location from users')
    results = cur.fetchall()

    return render_template('home.html', name=name, display=False, \
                           mylist=['one','two','three','four'], listofdictionaries=[{'name' : 'Solomon_Ondula'}, {'name' : 'Solomon_omusinde'}], results = results)

@app.route('/json') 
def json():
    if 'name' in session:
        name = session['name']
    else:
        name = 'NotinSession!'    
    return jsonify({'key': 'value', 'key2' : [1,2,3], 'name': name})

@app.route('/query')
def query():
    name = request.args.get('name')
    location = request.args.get('location')
    return '<h1>Hi {}, You are from {}. Welcome to the query page!</h1>'.format(name, location)

@app.route('/theform', methods=['GET', 'POST'])
def theform():

    if request.method == 'GET': 
        return render_template('form.html')   
    else:
        name = request.form['name']
        location = request.form['location']

        db = get_db()
        db.execute('insert into users (name, location) values (?, ?)', [name, location])
        db.commit()

        return redirect(url_for('home', name=name, location=location))


#@app.route('/process', methods=['POST'])
#def process():
    #name = request.form['name']
    #location = request.form['location']
    #return 'Hello {}, You are from {}. You have submitted the form successfully!'.format(name, location)


@app.route('/processjson', methods=['POST'])
def processjson():

    data = request.get_json()

    name = data['name']
    location = data['location']
    randomlist = data['randomlist']

    return jsonify({'result' : 'Success!', 'name':name, 'location':location, 'randomkeyinlist':randomlist[1]})

@app.route('/viewresults')
def viewresults():
    db = get_db()
    cur = db.execute('select id, name, location from users')
    results = cur.fetchall()
    return '<h1> The ID is {}. The name is {}. The location is {}.</h1>'.format(results[1]['id'], results[1]['name'], results[1]['location'])

if __name__ == '__main__':
    app.run()

