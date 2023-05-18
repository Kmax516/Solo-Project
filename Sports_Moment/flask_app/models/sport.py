from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user



class Sport:

    def __init__(self,data):
        self.id = data['id']
        self.Player_Name = data['Player_Name']
        self.Sport = data['Sport']
        self.Team = data['Team']
        self.Description = data['Description']
        self.Image = data['Image']
        self.Video = data['Video']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        # self.user_id = data['user_id']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO sports (Player_Name,Sport,Team,Description,Image,Video,user_id,created_at,updated_at) VALUES (%(Player_Name)s,%(Sport)s,%(Team)s,%(Description)s,%(Image)s,%(Video)s,%(user_id)s,Now(),Now());"
        return connectToMySQL("moment_schema").query_db(query,data)
    
    @staticmethod
    def validate_band(sport):
        is_valid = True
        query = "SELECT * FROM sports;"
        results = connectToMySQL("moment_schema").query_db(query,sport)
        if len(sport['Player_Name']) < 2:
            flash("Player name must be at least 2 characters",)
            is_valid= False
        if len(sport['Sport']) < 2:
            flash("Sport must be at least 2 characters",)
            is_valid= False
        if len(sport['Team']) < 2:
            flash("Team must be at least 2 character",)
            is_valid= False
        if len(sport['Description']) < 2:
            flash("Decription must be at least 2 character",)
            is_valid= False
        return is_valid
    
    @classmethod
    def delete(cls,data):
        query  = "DELETE FROM sports WHERE id = %(id)s;"
        
        return connectToMySQL("moment_schema").query_db(query, data)

    @classmethod
    def update(cls,data):
        query = "UPDATE sports SET Player_Name=%(Player_Name)s, Sport=%(Sport)s, Team=%(Team)s, Description=%(Description)s, Image=%(Image)s,Video=%(Video)s,updated_at = NOW(), created_at = Now() WHERE id = %(id)s;"
        return connectToMySQL("moment_schema").query_db(query,data)

    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM sports Join users on sports.user_id = users.id Where sports.id = %(id)s;"
        results = connectToMySQL("moment_schema").query_db(query,data)
        if len(results) == 0:
            return None
        else:
            # data = {'id':id}
            user_d = results[0]
            sport_object = cls(user_d)
            new_user_d = {
                'id' : user_d ['users.id'],
                'first_name': user_d['first_name'],
                'last_name' : user_d['last_name'],
                'email': user_d['email'],
                'password' : user_d['password'],
                'created_at' : user_d['users.created_at'],
                'updated_at' : user_d['users.updated_at']
             }
        
            user_object = user.User(new_user_d)
            sport_object.creator = user_object
       
            # return cls(results[0])
        return sport_object
    
    @classmethod
    def get_all(cls): # no data needed since grabbing all
        query = "SELECT * FROM sports Join users on sports.user_id = users.id;"
        results = connectToMySQL("moment_schema").query_db(query)
        if len(results) == 0:
            return []
        else:
            # 
            sport_object_list = []
            for user_d in results:
                print(user_d)
            
                sport_object = cls(user_d)
                new_user_d = {
                'id' : user_d ['users.id'],
                'first_name': user_d['first_name'],
                'last_name' : user_d['last_name'],
                'email': user_d['email'],
                'password' : user_d['password'],
                'created_at' : user_d['users.created_at'],
                'updated_at' : user_d['users.updated_at']
                }
        
                user_object = user.User(new_user_d)
                sport_object.creator = user_object
                sport_object_list.append(sport_object)
            return sport_object_list