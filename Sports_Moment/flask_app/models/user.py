from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_app.models.sport import Sport

class User:

    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.sports = []



    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL("moment_schema").query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL("moment_schema").query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("moment_schema").query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL("moment_schema").query_db(query,data)
        data = {'id':id}
        return cls(results[0])
    
    
    @classmethod
    def get_one_band(cls, data ): 
        query = "SELECT * FROM users LEFT JOIN sports on users.id = sports.user_id WHERE users.id = %(id)s;" 
        results = connectToMySQL("moment_schema").query_db(query,data) 
        print(results)  
        User = cls(results[0])  
        for row in results: 
            sport = { 
                'id': row['sports.id'],
                'Player_Name': row['Player_Name'],
                'Sport': row['Sport'],
                'Team': row['Team'],
                'Description': row['Description'],
                'Image': row['Image'],
                'Video': row['Video'],
                'created_at': row['sports.created_at'],
                'updated_at': row['sports.updated_at']
            }
            User.bands.append(Sport(sport))  
        return User









    @staticmethod
    def validate_user(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("moment_schema").query_db(query,user)
        if len(results) >= 1:
            flash("Email unusable.","regError",)
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Incorrect Email", "regError",)
            is_valid=False
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters", "regError",)
            is_valid= False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters", "regError")
            is_valid= False
        if len(user['password']) < 8:
            flash("Password must be no less then 8 characters", "regError")
            is_valid= False
        if user['password'] != user['verify']:
            flash("Passwords dont align","regError",)
        # if User.get_by_email(user):
        #     is_valid= False
        #     flash( "Choose another email", "regError")


        return is_valid

   