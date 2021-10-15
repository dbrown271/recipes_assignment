from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Users:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('recipes_schema').query_db(query)

        users = []

        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def verifed(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        results = connectToMySQL('recipes_schema').query_db(query, data)
        return results

    @staticmethod
    def verify(user):
        is_valid = True
        if len(user['first_name']) < 3:
            flash("First Name Requires More than 3 Characters.")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last Name Requires More than 3 Characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!")
            is_valid = False
        if len(user['email']) < 3:
            flash("Email Requires More than 3 Characters.")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password Requires More than 8 Characters.")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("The Password and Confirm Password Must Match!")
            is_valid = False

        return is_valid

    @staticmethod
    def verify_login(user):
        is_valid = True

        user_from_db = Users.get_by_email(user)
        if not user_from_db:
            flash("Wrong email or Password! Try Again!")
            is_valid = False

        elif bcrypt.check_password_hash(user_from_db.password, user['password']):
            flash("Wrong email or Password! Try Again!")
            is_valid = False
        
        return is_valid

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("recipes_schema").query_db(query,data)

        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users Where id = %(user_id)s;"
        result = connectToMySQL("recipes_schema").query_db(query,data)
        return cls( result[0] )
