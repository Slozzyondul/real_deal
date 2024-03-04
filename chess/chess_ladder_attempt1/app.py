from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
import random
import pickle

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'  # Change this to a secure secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Use SQLite for simplicity
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    id = db.Column(db.String(20), primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, default=1000)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class ChessLadder:
    def __init__(self):
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def display_ladder(self):
        sorted_players = Player.query.order_by(Player.rating.desc()).all()
        ladder_text = "Chess Ladder:<br>"
        for i, player in enumerate(sorted_players, start=1):
            ladder_text += f"{i}. {player.name} (Rating: {player.rating})<br>"
        return ladder_text

    def challenge(self, player1, player2):
        # Simulate a game and update ratings
        result = random.choice(["win", "draw", "loss"])
        if result == "win":
            player1.rating += 10
            player2.rating -= 10
        elif result == "loss":
            player1.rating -= 10
            player2.rating += 10
        # For a draw, no change in ratings

        db.session.commit()

        return f"{player1.name} vs {player2.name}: {result}"

    def save_players(self):
        db.session.commit()
        print("Player data saved.")

    def load_players(self):
        pass  # No need to load players from a file anymore

# Initialize the database
with app.app_context():
    db.create_all()

# Initialize the chess ladder
chess_ladder = ChessLadder()

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/")
@login_required
def index():
    ladder = chess_ladder.display_ladder()
    return render_template("index.html", ladder=ladder, username=current_user.username)

@app.route("/simulate_challenge", methods=["POST"])
@login_required
def simulate_challenge():
    # Simulate a challenge and update the ladder
    if len(Player.query.all()) < 2:
        return jsonify({"error": "Not enough players to simulate a challenge."})

    player1, player2 = random.sample(Player.query.all(), 2)
    result = chess_ladder.challenge(player1, player2)

    # Update the ladder display
    ladder = chess_ladder.display_ladder()

    return jsonify({"result": result, "ladder": ladder})

if __name__ == "__main__":
    app.run(debug=True)



