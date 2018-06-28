from config.db import query

def get_username():
    data = query("SELECT user_name FROM Users")
    return data

def insert_user(username, hashed, token):
    data = query("""INSERT INTO Users (user_name, user_hash, user_token) 
                    VALUES (%s, %s, %s);""", (username, hashed, token))
    return data

def get_hash(username):
    data = query("""SELECT user_hash FROM Users 
                    WHERE user_name = %s""", (username))
    return data[0]["user_hash"]

def add_token(token, username):
    data = query("""UPDATE Users SET user_token = %s 
                    WHERE user_name = %s""", (token, username))
    return data

def remove_token(user_id):
    data = query("""UPDATE Users SET user_token = %s 
                    WHERE user_id = %s""", (None, user_id))
    return data

def get_user_t(token):
    data = query("""SELECT user_id FROM users 
                    WHERE user_token = %s""",(token))
    return data