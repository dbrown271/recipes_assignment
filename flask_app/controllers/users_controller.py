from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models.users import Users
from flask_app.models.recipes import Recipes

from flask import flash

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def users():
    users = Users.get_all()
    print(users)
    return render_template('index.html', users=users)


@app.route('/register', methods=['POST'])
def user_data():
    if not Users.verify(request.form):
        return redirect('/')

    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password']),
    }

    user_id = Users.verifed(data)
    session['user_id'] = user_id

    return redirect('/dashboard')


@app.route("/login", methods=['POST'])
def login():

    if not Users.verify_login(request.form):
        return redirect('/')

    user_from_db = Users.get_by_email(request.form)

    session['user_id'] = user_from_db.id

    return redirect('/dashboard')

@app.route("/dashboard")
def dashboard_page():
    if "user_id" not in session:
        flash("Please Register/Login!")
        return redirect ("/")

    data = {
        "user_id" : session['user_id']
    }

    user = Users.get_by_id(data)
    all_recipes = Recipes.users_with_recipes()

    return render_template('dashboard.html', user = user, all_recipes = all_recipes)














@app.route("/clear_session")
def clear_session():
    session.clear()
    return redirect("/")