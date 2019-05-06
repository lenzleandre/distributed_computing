import os, sqlite3, json
from flask import Flask, request, jsonify
from datetime import datetime



app = Flask(__name__, instance_relative_config=True)
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

now = datetime.now()
time = now.strftime('%H:%M:%S')

#Friend_DB creation with two tables

conn = sqlite3.connect(app.instance_path + '/message_DB.db')
cur = conn.cursor()
message_sql= """CREATE TABLE IF NOT EXISTS charts(
 chart_id INTEGER PRIMARY KEY AUTOINCREMENT,
 msg_time datetime,
 usernamea char[25] NOT NULL,
 messagea CLOB,
 messageb CLOB,
 usernameb char[25] NOT NULL  
); """

cur.execute(message_sql)

conn.close()

#Writting a message
@app.route('/message', methods=['POST'])
def write_message():
    if request.method == 'POST':
        try:
            print(request.form)
            msg_time = request.form.get('msg_time')
            usernamea = request.form.get('usernamea')
            messagea = request.form.get('messagea')
            messageb = request.form.get('messageb')
            usernameb = request.form.get('usernameb')

            print(msg_time, usernamea, messagea, messageb, usernameb)
            conn = sqlite3.connect(app.instance_path + '/message_DB.db')
            cur = conn.cursor()
            cur.execute(''' INSERT INTO charts(msg_time, usernamea, messagea, messageb, usernameb) VALUES (?, ?, ?, ?,?)''', (time, usernamea, messagea,messageb, usernameb));
            cur.execute(''' INSERT INTO charts(msg_time, usernamea, messagea, messageb, usernameb) VALUES (?, ?, ?, ?,?)''', (time, usernameb, messageb, messagea, usernamea));
            conn.commit()
            conn.close()
            return '', 200
        except sqlite3.Error as e:
            print('error %s' % e.args[0])
        return'', 400

@app.route('/message/<usernamea>', methods=['GET'])
def received_message(usernamea):
    try:
        print(usernamea)
        conn = sqlite3.connect(app.instance_path + '/message_DB.db')
        cur = conn.cursor()
        messages = """ SELECT DISTINCT charts.msg_time, charts.messagea, charts.messageb,charts.usernameb, charts.msg_time FROM charts WHERE charts.usernamea = (?) """;
        cur.execute(messages, [usernamea])
        all_records = cur.fetchall()
        all_records.sort() # in_records + out_records
        conn.close()
        return json.dumps(all_records), 200
    except sqlite3.Error as e:
        print('error %s' % e.args[0])
    return '', 400


if __name__ == '__main__':
    app.run(debug=True)
