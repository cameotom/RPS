from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.match import Match
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) # we are creating an object called bcrypt,
                         # which is made by invoking the function Bcrypt with our app as an argument

@app.route('/matches/new')
def dashboard():
    if 'user_id' not in session:
        print("user id not in session")
        return redirect('/user/logout')
    data = {
        'user_id': session['user_id']
    }
    return render_template("matches_new.html", user = User.get_user_by_id(data), unmatched_users = Match.get_unmatched_users(data))


@app.route('/match/<int:id>')
def make_match(id):
    if 'user_id' not in session:
        return redirect('/user/logout')
    data = {
        "user1_id": session["user_id"],
        "user2_id": id
    }
    Match.create_match(data)
    return redirect('/matches')

@app.route('/matches')
def view_existing_matches():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "user_id": session['user_id']
    }
    return render_template("matches.html", user = User.get_user_by_id(data), matched_users = Match.get_matched_users(data))