from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
import re	# the regex module
# create a regular expression object that we'll use later
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash


class Match:
    def __init__( self , data ):
        self.id = data['id']
        self.user1_id = data['user1_id']
        self.user2_id = data['user2_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user1_wins = data['user1_wins']
        self.user2_wins = data['user2_wins']
        self.ties = data['ties']
        self.active_game = data['active_game']
        self.player = 0
        self.opponent = None

    @classmethod
    def get_unmatched_users(cls, data):
        query = "select * from user where id != %(user_id)s and id not in (select user.id from matches join user on user.id=matches.user1_id OR user.id = matches.user2_id where user.id!=%(user_id)s and (user1_id=%(user_id)s OR user2_id=%(user_id)s));"
        result = connectToMySQL('rps').query_db(query, data)
        if len(result) < 1:
            return False
        return result

    @classmethod
    def create_match(cls, data):
        query = "INSERT INTO matches (user1_id, user2_id, created_at, updated_at) VALUES(%(user1_id)s,%(user2_id)s,NOW(),NOW());"
        return connectToMySQL('rps').query_db(query, data)

    @classmethod
    def get_matches(cls, data):
        query = "SELECT * FROM matches where user1_id=%(user_id)s OR user2_id=%(user_id)s;"
        result = connectToMySQL('rps').query_db(query, data)
        if len(result) < 1:
            return False
        return result

    @classmethod
    def get_matched_users(cls, data):
        query = "select * from matches join user on user.id=matches.user1_id OR user.id = matches.user2_id where user.id!=%(user_id)s and (user1_id=%(user_id)s OR user2_id=%(user_id)s) "
        result = connectToMySQL('rps').query_db(query, data)
        if len(result) < 1:
            return False
        matched_users = []
        for row in result:
            matched_user = cls(row)
            matched_user.active_game = row["active_game"] if row["active_game"] != None else 0
            matched_user.opponent = user.User({
                "id": row["user.id"],
                "name": row["name"],
                "email": row["email"],
                "password": None,
                "created_at": row["created_at"],
                "updated_at": row["updated_at"]
            })
            if matched_user.user1_id == data["user_id"]:
                matched_user.player = 1
            else:
                matched_user.player= 2
            matched_users.append(matched_user)
        return matched_users

    @classmethod
    def get_one_matched_user(cls, data):
        query = "SELECT * FROM matches join user on user.id=matches.user1_id OR user.id = matches.user2_id where user.id!=%(user_id)s and matches.id=%(match_id)s and (user1_id=%(user_id)s OR user2_id=%(user_id)s);"
        result = connectToMySQL('rps').query_db(query, data)
        if len(result) < 1:
            return False
        return result

    @classmethod
    def get_record(cls, data):
        query = "select game.winner, count(*) from matches left join game on game.match_id=matches.id where matches.id = %(match_id) group by game.winner order by game.winner;"
        result = connectToMySQL('rps').query_db(query, data)
        print(result)