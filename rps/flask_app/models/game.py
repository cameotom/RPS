from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
from flask_app.models.match import Match
import re	# the regex module
# create a regular expression object that we'll use later
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash


class Game:
    def __init__( self , data ):
        self.id = data['id']
        self.winner = data['winner']
        self.match_id = data['match_id']
        self.user1_move = data['user1_move']
        self.user2_move = data['user2_move']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        #self.opponent = None

    @classmethod
    def create_game(cls, data):
        query = "INSERT into game (match_id, created_at, updated_at) VALUES (%(match_id)s, NOW(), NOW())"
        result = connectToMySQL('rps').query_db(query, data)
        query2 = "UPDATE matches set active_game = %(id)s where id=%(match_id)s;"
        result2 = connectToMySQL('rps').query_db(query2, {"id": result, "match_id": data["match_id"]})
        return result

    @classmethod
    def which_player(cls, data):
        query = "SELECT * from game join matches on matches.id=game.match_id where game.id=%(game_id)s"
        result = connectToMySQL('rps').query_db(query, data)
        for row in result:
            data2 = {
                "user1_id": row['user1_id'],
                "user2_id": row['user2_id']
            }
        if data2["user1_id"] == data["user_id"]:
            print("its user1")
            return 1
        if data2["user2_id"] == data["user_id"]:
            print("its user2")
            return 2
        else:
            print("who are you?")
            return false

    @classmethod
    def get_game(cls, data):
        query = "select * from game where id=%(game_id)s;"
        result = connectToMySQL('rps').query_db(query, data)
        game = cls(result[0])
        return game

    @classmethod
    def make_move(cls, data):
        #sets the move the player made and sets who went
        if data["player"] == 1:
            query = "UPDATE game set user1_move = %(move)s, updated_at = NOW() where id=%(game_id)s;"
            result = connectToMySQL('rps').query_db(query, data)
        else:
            query = "UPDATE game set user2_move = %(move)s, updated_at = NOW() where id=%(game_id)s;"
            result = connectToMySQL('rps').query_db(query, data)
        Game.bothWent(data)
        return True

    @classmethod
    def bothWent(cls, data):
        # tells us if both players have gone
        query = "select * from game where id=%(game_id)s;"
        result = connectToMySQL('rps').query_db(query, data)
        game = cls(result[0])
        if game.user1_move is not None and game.user2_move is not None:
            query2 = "Update matches set active_game=0 where id=%(match_id)s"
            result2 = connectToMySQL('rps').query_db(query2, data)
            Game.winner(game)
            return 1
        else:
            return 0

    # @classmethod
    # def bothWent2(cls, data):
    #     #tells us if both players have gone
    #     query2 = "select user1_move, user2_move from game where id=%(game_id)s;"
    #     result2 = connectToMySQL('rps').query_db(query2, data)
    #     if result2[0]["user1_move"] is not None and result2[0]["user2_move"] is not None:
    #         query3 = "Update matches set active_game=0 where id=%(match_id)s"
    #         result3 = connectToMySQL('rps').query_db(query3, data)
    #         Game.winner(data)
    #         return 1
    #     else:
    #         return 0

    @classmethod
    def winner(cls, game):
        #tells us who won
        p1 = game.user1_move.upper()[0]#just want the first letter of the move from rock, paper or scissors. so r, p, s
        p2 = game.user2_move.upper()[0]
        data = {
            "user1_move": game.user1_move,
            "user2_move": game.user2_move,
            "game_id": game.id,
            "match_id": game.match_id
        }
        if p1 == "R" and p2 == "S":
            Game.winner1(data)
        elif p1 == "P" and p2 =="R":
            Game.winner1(data)
        elif p1 == "S" and p2 == "P":
            Game.winner1(data)
        elif p1 == "R" and p2 =="P":
            Game.winner2(data)
        elif p1 == "P" and p2 == "S":
            Game.winner2(data)
        elif p1 == "S" and p2 == "R":
            Game.winner2(data)
        else:
            Game.tie(data)
        return True

    @classmethod
    def winner1(cls, data):
        query = "UPDATE game SET winner=1 where id=%(game_id)s;"
        result = connectToMySQL('rps').query_db(query, data)
        query2 = "UPDATE matches SET user1_wins= user1_wins + 1 where id=%(match_id)s;"
        result2 = connectToMySQL('rps').query_db(query2, data)
        return True

    @classmethod
    def winner2(cls, data):
        query = "UPDATE game SET winner=2 where id=%(game_id)s;"
        result = connectToMySQL('rps').query_db(query, data)
        query2 = "UPDATE matches SET user2_wins= user2_wins + 1 where id=%(match_id)s;"
        result2 = connectToMySQL('rps').query_db(query2, data)
        return True

    @classmethod
    def tie(cls, data):
        query = "UPDATE game SET winner=-1 where id=%(game_id)s;"
        result = connectToMySQL('rps').query_db(query, data)
        query2 = "UPDATE matches SET ties= ties + 1 where id=%(match_id)s;"
        result2 = connectToMySQL('rps').query_db(query2, data)
        return True