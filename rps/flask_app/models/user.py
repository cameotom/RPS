from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	# the regex module
# create a regular expression object that we'll use later
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash



# model the class after the user table from our database
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @staticmethod
    def validate_registration(user):
        is_valid = True
        query = "SELECT * FROM user WHERE email = %(email)s;"
        results = connectToMySQL('rps').query_db(query, user)
        if len(results) >= 1:
            flash("Email already taken", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email", "register")
            is_valid = False
        if len(user['name']) < 2:
            flash("Username must be at least 2 characters")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid = False
        if user['password'] != user['password2']:
            flash("Passwords don't match", "register")
        return is_valid

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO user (name,email,password, created_at, updated_at) VALUES(%(name)s,%(email)s,%(password)s, NOW(), NOW())"
        return connectToMySQL('rps').query_db(query, data)

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM user where email = %(email)s;"
        result = connectToMySQL('rps').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM user where id = %(user_id)s;"
        result = connectToMySQL('rps').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM user;"
        result = connectToMySQL('rps').query_db(query)
        return result

    @staticmethod
    def validate_edit_username(data):
            is_valid = True
            if len(data['name']) < 3:
                flash("Username must be at least 3 characters")
                is_valid = False
            return is_valid

    @staticmethod
    def validate_edit_password(data):
        is_valid = True
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid = False
        if data['password'] != data['password2']:
            flash("Passwords don't match", "register")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_delete_account(data):
        is_valid = True
        if data['confirmation'] != "DELETE":
            flash("You must write DELETE in the box to confirm you want to delete your account. This is case sensitive.", "delete")
            is_valid = False
        return is_valid

    @classmethod
    def update_username(cls, data):
        query = "UPDATE user SET name = %(name)s, updated_at = NOW() where id=%(user_id)s;"
        return connectToMySQL('rps').query_db(query, data)

    @classmethod
    def update_password(cls, data):
        query = "UPDATE user SET password= %(password)s, updated_at = NOW() where id=%(user_id)s;"
        return connectToMySQL('rps').query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM user WHERE id=%(user_id)s;"
        return connectToMySQL('rps').query_db(query, data)

