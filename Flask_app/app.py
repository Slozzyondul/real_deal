from flask import Flask, jsonify, request, url_for, redirect, session

app = Flask(__name__)

app.config['DEBUG'] = True

app.config['SECRET_KEY'] = 'secret!'

@app.route('/')
def index():
    session.pop('name', None)
    return '<h1>Welcome To Solomon Ondula Page!</h1>'

@app.route('/home', methods=['POST', 'GET'], defaults={'name': 'anonymous'})
@app.route('/home/<string:name>', methods=['POST', 'GET'])
def home(name):

    session['name'] = name

    return '<h1>Welcome {}, to Solomon home page!</>'.format(name)

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
        return '''<form method="POST" action="/theform">
                    <input type="text" name="name">
                    <input type="text" name="location">
                    <input type="submit" value="Submit">
                </form>'''    
    else:
        name = request.form['name']
        location = request.form['location']

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

if __name__ == '__main__':
    app.run()

