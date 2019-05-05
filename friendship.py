
'''Friendship functionalities handler '''

import os
from flask import Flask, request, json
import sqlite3


app = Flask(__name__, instance_relative_config=True)
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

#Friend_DB creation

db_con = sqlite3.connect(app.instance_path + '/friend_DB.db')
cursor = db_con.cursor()
create_table_sql = """ CREATE TABLE IF NOT EXISTS friends (
usernamea text NOT NULL,
usernameb text NOT NULL,
PRIMARY KEY (usernamea, usernameb)
        ); """
cursor.execute(create_table_sql)
db_con.close()


# Reading friends of a given user

@app.route('/friends/<usernamea>', methods=['GET'])
def read_friend(usernamea):
    try:
        print(usernamea)
        db_con = sqlite3.connect(app.instance_path + '/friend_DB.db')
        cursor = db_con.cursor()
        sql_read_friend = ''' SELECT usernameb FROM friends WHERE usernamea = (?) '''
        cursor.execute(sql_read_friend, [usernamea])
        user_friends =cursor.fetchall()
        friends_list = []
        for i in user_friends:
            friends_list +=i
        db_con.close()
        return json.dumps(friends_list), 200
    except sqlite3.Error as e:
        print('error %s' % e.args[0])
    return '', 400


# create relationship inter-users a & b : friendship

@app.route('/friends', methods=['POST'])
def create_friend():
    if request.method == 'POST':
        try:
            print(request.form)

            usernamea = request.form.get('usernamea')
            usernameb = request.form.get('usernameb')
            print(usernamea, usernameb)
            db_con = sqlite3.connect(app.instance_path + '/friend_DB.db')
            cursor = db_con.cursor()
            cursor.execute('''INSERT INTO friends (usernamea, usernameb) VALUES (?, ?)''', (usernamea, usernameb))
            cursor.execute('''INSERT INTO friends (usernamea, usernameb) VALUES (?, ?)''', (usernameb, usernamea))
            db_con.commit()
            db_con.close()
            return '', 200
        except sqlite3.Error as e:
            print('error %s' % e.args[0])
        return '', 400

# remove a friendship from the given friend couple

@app.route('/friends', methods=['DELETE'])
def delete_friend():
    if request.method == 'DELETE':
        try:
            print(request.form)

            usernamea = request.form.get('usernamea')
            usernameb = request.form.get('usernameb')
            print(usernamea, usernameb)
            db_con = sqlite3.connect(app.instance_path + '/friend_DB.db')
            cursor = db_con.cursor()
            cursor.execute('''DELETE FROM friends WHERE usernamea = (?) AND usernameb = (?)''', (usernamea, usernameb))
            cursor.execute('''DELETE FROM friends WHERE usernamea= (?) AND usernameb = (?)''', (usernameb, usernamea))
            db_con.commit()
            db_con.close()
            return '', 200
        except sqlite3.Error as e:
            print('error %s' % e.args[0])
        return '', 400


if __name__ == '__main__':
    app.run(debug=True)
