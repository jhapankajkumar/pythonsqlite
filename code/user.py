import sqlite3
from flask_restful import Resource, reqparse
from flask import Flask, request


class User(object):
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def get_user_by_username(cls, username):
        # Connect to database
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        print(cursor)
        print(connection)

        # Get_user _query
        query = "SELECT * from users WHERE username=?"
        results = cursor.execute(query, (username,))
        print(query)
        # Fetch single row
        result = results.fetchone()
        if result:
            # Create user using row data
            user = cls(*result)
        else:
            user = None
        # Close connection
        connection.close()
        return user

    @classmethod
    def get_user_by_id(cls, _id):
        # Connect to database
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # Get_user _query
        get_user = "SELECT * from users WHERE id=?"
        results = cursor.execute(get_user, (_id,))

        # Fetch single row
        result = results.fetchone()

        if result:
            # Create user using row data
            user = User(*result)
        else:
            user = None

        # Close connection
        connection.close()
        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field can not be blank"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field can not be blank"
                        )

    def post(self):

        data = UserRegister.parser.parse_args()
        user = User.get_user_by_username(data['username'])
        if user:
            return {"message": "User is already added"}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO users VALUES(NULL,?,?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message": "You have registered successfully"}, 201
