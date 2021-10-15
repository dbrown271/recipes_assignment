from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.controllers.users_controller import Users
from flask import flash

from flask_app.models.recipes import Recipes
from flask_app.models.users import Users




@app.route("/add_new_recipes")
def add_new_recipes():
    if "user_id" not in session:
        flash("Please register/login before continuing.")
        return redirect('/')

    data = {
        "user_id" : session['user_id']
    }

    user = Users.get_by_id(data)

    return render_template("add_new_recipes.html", user = user)


@app.route("/save_recipes", methods=['POST'])
def save_recipes():
    if "user_id" not in session:
        flash("Please register/login before continuing.")
        return redirect('/')
    if not Recipes.verify_recipes(request.form):
        return redirect('/add_new_recipes')

    data = {
        "dish_name": request.form['dish_name'],
        "dish_description": request.form['dish_description'],
        "dish_time": request.form['dish_time'],
        "dish_instructions": request.form['dish_instructions'],
        "user_id": session['user_id'],
    }

    Recipes.insert_recipe(data)

    return redirect("/dashboard")

@app.route("/show/<int:recipe_id>")
def show_recipe(recipe_id):
    if"user_id" not in session:
        flash("please register/login before continuing!")
        return redirect('/')

    data = {
        "recipe_id": recipe_id
    }

    recipe = Recipes.one_user_one_recipe(data)

    return render_template("show_recipe.html", recipe = recipe )


@app.route('/edit_recipes/<int:recipe_id>')
def edit_recipe(recipe_id):
    if "user_id" not in session:
        flash("Please register/login before continuing.")
        return redirect('/')
    data = {
        "recipe_id": recipe_id
    }

    recipe = Recipes.one_user_one_recipe(data)

    return render_template("edit_recipes.html", recipe = recipe)


@app.route('/update/<int:recipe_id>', methods =['POST'])
def update_recipe(recipe_id):

    if not Recipes.verify_recipes(request.form):
        return redirect('/edit_recipe/f{recipe_id}')

    data = {
        "dish_name": request.form['dish_name'],
        "dish_description": request.form['dish_description'],
        "dish_time": request.form['dish_time'],
        "dish_instructions": request.form['dish_instructions'],
        "recipe_id" : recipe_id
    }
    Recipes.update_recipe(data)
    return redirect("/dashboard")

@app.route("/delete/<int:recipe_id>")
def delete_recipe(recipe_id):

    data = {
        "recipe_id" : recipe_id
    }

    Recipes.delete_recipe(data)

    return redirect('/dashboard')
