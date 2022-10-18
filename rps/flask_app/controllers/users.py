from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.match import Match
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) # we are creating an object called bcrypt,
                         # which is made by invoking the function Bcrypt with our app as an argument

@app.route('/')
def index():
    return redirect('/login')

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/user/create', methods=["POST"])
def user_create():
    # First we make a data dictionary from our request.form coming from our template.
    # The keys in data need to line up exactly with the variables in our query string.
    if not User.validate_registration(request.form):
        return redirect('/register')
    hashed_password = bcrypt.generate_password_hash(request.form["password"])
    data = {
        "name": request.form["name"],
        "email": request.form["email"],
        "password": hashed_password
    }
    # We pass the data dictionary into the save method from the user class.
    user_id = User.create_user(data)
    session['user_id'] = user_id
    # Don't forget to redirect after saving to the database.
    return redirect('/matches/new')

@app.route('/user/login', methods=["POST"])
def user_login():
    user_in_db = User.get_user_by_email(request.form)
    if not user_in_db:
        flash("Email not registered")
        return redirect('/login')
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("Invalid Password")
        return redirect('/login')
    session['user_id'] = user_in_db.id
    return redirect('/matches/new')

@app.route('/users')
def users():
    users = User.get_all_users()
    return render_template("users.html", users = users)

@app.route('/user/logout')
def user_logout():
    session.clear()
    return redirect('/')

@app.route('/user/edit/<int:id>')
def user_edit(id):
    data = {
        "user_id": id
    }
    return render_template("edit_account.html", user = User.get_user_by_id(data))

@app.route('/user/edit/username', methods=['POST'])
def edit_user():
    user_id = request.form["user_id"]
    if not User.validate_edit_username(request.form):
        return redirect(f"/user/edit/{user_id}")
    data = {
        "user_id": request.form["user_id"],
        "name": request.form["name"]
    }
    User.update_username(data)
    return redirect(f"/user/edit/{user_id}")

@app.route('/user/edit/password', methods=['POST'])
def edit_password():
    user_id = request.form["user_id"]
    if not User.validate_edit_password(request.form):
        return redirect(f"/user/edit/{user_id}")
    hashed_password = bcrypt.generate_password_hash(request.form["password"])
    data = {
        "user_id": request.form["user_id"],
        "password": hashed_password
    }
    User.update_password(data)
    return redirect(f"/user/edit/{user_id}")

@app.route('/user/delete', methods=['POST'])
def user_delete():
    user_id = request.form["user_id"]
    if not User.validate_delete_account(request.form):
        return redirect(f"/user/edit/{user_id}")
    data = {
        "user_id": request.form["user_id"]
    }
    User.delete(data)
    return redirect('/register')
