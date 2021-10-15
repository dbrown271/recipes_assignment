from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import users



class Recipes:
    def __init__(self, data):
        self.id = data["id"]
        self.dish_name = data["dish_name"]
        self.dish_description = data["dish_description"]
        self.dish_time = data["dish_time"]
        self.dish_instructions = data["dish_instructions"]
        self.user_id = data["user_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        self.owner = {}

    @staticmethod
    def verify_recipes(my_recipes):
        is_valid = True

        if len(my_recipes['dish_name']) < 3:
            flash("Title must be at least 3 characters long!")
            is_valid = False

        if len(my_recipes['dish_description']) < 3:
            flash("Description must be at least 3 characters long!")
            is_valid = False

        if len(my_recipes['dish_instructions']) < 3:
            flash("Description must be at least 3 characters long!")
            is_valid = False

        return is_valid

    @classmethod
    def insert_recipe(cls, data):
        query = "INSERT INTO recipes (dish_name, dish_description, dish_time, dish_instructions, user_id, created_at, updated_at) VALUES (%(dish_name)s, %(dish_description)s, %(dish_time)s, %(dish_instructions)s, %(user_id)s, NOW(), NOW());"
        results = connectToMySQL("recipes_schema").query_db(query, data)
        return results

    @classmethod
    def users_with_recipes(cls):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id;"
        results = connectToMySQL("recipes_schema").query_db(query)

        all_recipes = []

        for row in results:
            one_recipe = cls(row)
            user_data = {
                "id" : row['users.id'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'],
                "email" : row['email'],
                "password" : row['password'],
                "created_at" : row['users.created_at'],
                "updated_at" : row['users.updated_at'],
            }
            one_recipe.owner = users.Users(user_data)
            all_recipes.append(one_recipe)
        return all_recipes

    @classmethod
    def one_user_one_recipe(cls, data):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(recipe_id)s;"
        results = connectToMySQL("recipes_schema").query_db(query, data)

        one_recipe = cls(results[0])

        user_data = {
                "id" : results[0]['users.id'],
                "first_name" : results[0]['first_name'],
                "last_name" : results[0]['last_name'],
                "email" : results[0]['email'],
                "password" : results[0]['password'],
                "created_at" : results[0]['users.created_at'],
                "updated_at" : results[0]['users.updated_at'],
        }

        one_recipe.owner = users.Users(user_data)
        return one_recipe

    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET dish_name = %(dish_name)s, dish_description = %(dish_description)s, dish_time = %(dish_time)s, dish_instructions = %(dish_instructions)s, updated_at = NOW() WHERE id = %(recipe_id)s;"
        results = connectToMySQL("recipes_schema").query_db(query, data)
        return 
    
    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id=%(recipe_id)s;"
        results = connectToMySQL("recipes_schema").query_db(query, data)
        return