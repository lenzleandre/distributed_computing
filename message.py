
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
message_sql_a = """CREATE TABLE IF NOT EXISTS charts_a (
 chart_id INTEGER PRIMARY KEY AUTOINCREMENT,
 msg_time_a datetime,
 usernamea text NOT NULL,
 messagea CLOB,
 messageb CLOB,
 usernameb text NOT NULL   
); """

message_sql_b = """CREATE TABLE IF NOT EXISTS charts_b (
 chart_id INTEGER PRIMARY KEY AUTOINCREMENT,
 msg_time_b datetime,
 usernamea text NOT NULL,
 messagea CLOB,
 messageb CLOB,
 usernameb text NOT NULL   
); """
cur.execute(message_sql_b)
cur.execute(message_sql_a)

conn.close()

#Writting a message
@app.route('/message', methods=['POST'])
def write_message():
    if request.method == 'POST':
        try:
            print(request.form)
            msg_time_a = request.form.get('msg_time_a')
            msg_time_b = request.form.get('msg_time_b')
            usernamea = request.form.get('usernamea')
            messagea = request.form.get('messagea')
            messageb = request.form.get('messageb')
            usernameb = request.form.get('usernameb')

            print(msg_time_a, usernamea, messagea, messageb, usernameb, msg_time_b)
            conn = sqlite3.connect(app.instance_path + '/message_DB.db')
            cur = conn.cursor()

            #INSERT INTO charts_a(msg_time_a, usernamea, messagea, messageb, usernameb) VALUES('22:50', 'MARRY','hey frnd', '', 'john');
            #INSERT INTO charts_b(msg_time_b, usernamea, messagea, messageb, usernameb) VALUES('22:50', 'john','', 'hey frnd', 'MARRY');

            cur.execute(''' INSERT INTO charts_a(msg_time_a, usernamea, messagea, messageb, usernameb) VALUES (?, ?, ?, ?,?)''', (time, usernamea, messagea,messageb, usernameb));
            cur.execute(''' INSERT INTO charts_b(msg_time_b, usernamea,messagea, messageb, usernameb) VALUES (?, ?, ?, ?,?)''', (time, usernameb, messageb, messagea, usernamea));

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

        #SELECT DISTINCT charts_a.msg_time_a, charts_a.messageb, charts_a.messagea, charts_b.usernamea,charts_b.msg_time_b FROM charts_a, charts_b WHERE charts_a.usernamea ='marry';

        messages_a = """ SELECT DISTINCT charts_a.msg_time_a, charts_a.messageb, charts_a.messagea, charts_b.usernamea,charts_b.msg_time_b FROM charts_a, charts_b WHERE charts_a.usernamea = (?) """;
        #messages_a = """ SELECT DISTINCT charts_a.msg_time_a, charts_a.messagea, charts_b.messagea,charts_b.usernamea, charts_b.msg_time_b FROM charts_a,charts_b WHERE charts_a.usernamea = (?) """;

        #SELECT DISTINCT charts_b.msg_time_b, charts_b.messagea, charts_b.messageb, charts_b.usernameb,charts_a.msg_time_a FROM charts_a, charts_b WHERE charts_b.usernamea ='leandre';
        messages_b = """SELECT DISTINCT charts_b.msg_time_b, charts_b.messagea, charts_b.messageb, charts_b.usernameb,charts_a.msg_time_a FROM charts_a, charts_b WHERE charts_b.usernamea = (?) """;

        cur.execute(messages_a, [usernamea])
        cur.execute(messages_b, [usernamea])

        all_records = cur.fetchall()
        all_records.sort() # in_records + out_records
        conn.close()
        return json.dumps(all_records), 200
    except sqlite3.Error as e:
        print('error %s' % e.args[0])
    return '', 400


if __name__ == '__main__':
    app.run(debug=True)