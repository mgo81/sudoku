from config.db import query

def get_user(token):
    data = query("""SELECT user_id FROM users 
                    WHERE user_token = %s""",(token))
    return data

def get_difficulty(difficulty):
    data = query("""SELECT difficulty_id FROM difficulties 
                    WHERE difficulty_name = %s""", (difficulty))
    return data

def get_hiscores(cat_string, cat_value):
    data = query("""SELECT hiscores.hiscore_time, users.user_name, difficulties.difficulty_name 
        FROM hiscores 
        INNER JOIN users ON users.user_id = hiscores.hiscore_user_id
        INNER JOIN difficulties ON difficulties.difficulty_id = hiscores.hiscore_difficulty
        """ + cat_string + """
        ORDER BY hiscores.hiscore_time
        LIMIT 10""", tuple(cat_value))
    return data
def insert_hiscore(user, score, difficulty_id):
    data = query("""INSERT INTO Hiscores (hiscore_user_id, hiscore_time, hiscore_difficulty) 
                    VALUES (%s, %s, %s)""", (user, score, difficulty_id))
    return data