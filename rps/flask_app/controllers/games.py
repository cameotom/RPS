from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.match import Match
from flask_app.models.game import Game
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) # we are creating an object called bcrypt,
                         # which is made by invoking the function Bcrypt with our app as an argument

@app.route('/create_game', methods=["POST"])
def create_game():
    data = {
        "id": session['user_id'],
        "match_id": request.form['match_id']
    }
    game_id = Game.create_game(data)
    return redirect(f"/game/{data['match_id']}/{game_id}")

@app.route('/game/<int:match_id>/<int:game_id>')
def game(match_id, game_id):
    if 'user_id' not in session:
        print("user id not in session")
        return redirect('/user/logout')
    data = {
        "game_id": game_id,
        "user_id": session['user_id'],
        "match_id": match_id
    }
    return render_template("game.html", user = User.get_user_by_id(data), opponent = Match.get_one_matched_user(data), game = Game.get_game(data), player = Game.which_player(data))

@app.route('/make_move/<int:game_id>/<int:player>/Rock', methods=["POST"])
def Rock(game_id, player):
    data = {
        "user_id": session['user_id'],
        "game_id": game_id,
        "player": player,
        "move": "Rock",
        "match_id": request.form['match_id']
    }
    Game.make_move(data)
    return redirect("/matches")

@app.route('/make_move/<int:game_id>/<int:player>/Paper', methods=["POST"])
def Paper(game_id, player):
    data = {
        "user_id": session['user_id'],
        "game_id": game_id,
        "player": player,
        "move": "Paper",
        "match_id": request.form['match_id']
    }
    Game.make_move(data)
    return redirect("/matches")

@app.route('/make_move/<int:game_id>/<int:player>/Scissors', methods=["POST"])
def Scissors(game_id, player):
    data = {
        "user_id": session['user_id'],
        "game_id": game_id,
        "player": player,
        "move": "Scissors",
        "match_id": request.form['match_id']
    }
    Game.make_move(data)
    return redirect("/matches")