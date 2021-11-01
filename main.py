from flask import Flask, request, session, escape, jsonify
import pymysql
import os
import hashlib

#local connection
# db = pymysql.connect(host='localhost',user='root',password='zhong',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

# docker connection
db = pymysql.connect(host='db', user='root', password=os.getenv(
    'MYSQL_PASSWORD'), db='zhong', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

cur = db.cursor()
cur.execute("create database IF NOT EXISTS zhong")
cur.execute("use zhong")

cur.execute("create table IF NOT EXISTS user(username varchar(200), password varchar(200),family_contact varchar(200), doctor_contact varchar(200))")

app = Flask(__name__)

print("start!!!!!!!!!!!!")
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        print("data received from login:")
        username = request.form.get('username')
        password = request.form.get('password')
        print(username)
        print(password)
        sql = "select * from user where username = (%s)"
        cur.execute(sql, username)
        name = cur.fetchone()
        if name is None:
            return "username not exists"

        if name['password'] == password:
            return "successful"
        else:
            return "login failed"

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        print("data received from sign up: ")
        username = request.form.get('username')
        password = request.form.get('password')
        family_contact = request.form.get('family_contact')
        doctor_contact = request.form.get('doctor_contact')
        print(username)
        print(password)
        print(family_contact)
        print(doctor_contact)
        sql = "insert into user(username, password, family_contact, doctor_contact) values (%s,%s,%s,%s)"
        cur.execute(sql,(username,password,family_contact,doctor_contact))
        db.commit()
        return "success"

        # return {'message':'success','user':username}
    else:
        print("bad request")
        # return {"b":"fail"}
        return "fail"
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
