import mysql.connector
import json
from flask import make_response
from datetime import datetime,timedelta
import jwt
class user1():
    def __init__(self):
        try:
            self.con=mysql.connector.connect(host="localhost",user="root",
            password="mysql",database="flask_tutorial")
            self.con.autocommit=True
            self.cur=self.con.cursor(dictionary=True)
            print("connection established")
        except:
            print("error")
    def user_getall(self):
        self.cur.execute("select * from users")
        result=self.cur.fetchall()
        if len(result)>0:
             return make_response({"Data":result},200)
        else :
            return {"Message":"no data found"}
    def user_setall(self,data):
        self.cur.execute("INSERT INTO users (name, email, phone, role, password) VALUES (%s, %s, %s, %s, %s)",
        (data['name'], data['email'], data['phone'], data['role'], data['password']))
        
        return make_response({"message":"details entered"},201)
    def user_updateall(self,data):
        self.cur.execute("update users set password=%s where user_id=%s",(data['password'],data['user_id']))
        if self.cur.rowcount>0:
            return make_response({"message":"details updated"},201)
        else:
             return make_response({"message":"NOthing to updated"},202)
    def user_deleteall(self,data):
        self.cur.execute("delete from users where user_id=%s",(data['user_id'],))
        
        return {"message":"details deleted"}
    def user_pagination(self,limit,page):
        limit=int(limit)
        page=int(page)
        start=(page*limit)-limit
        qry=f"select * from users LIMIT {start},{limit}"
        self.cur.execute(qry)
        result=self.cur.fetchall()
        if len(result)>0:
             return make_response({"Data":result,"page_no":page,"limit":limit},200)
        else :
            return {"Message":"no data found"}
    def user_upload_model(self,uid,filepath):
        self.cur.execute("update users set avatar=%s where user_id=%s",(filepath,uid))
        if self.cur.rowcount>0:
            return make_response({"message":"file uploaded"},201)
        else:
             return make_response({"message":"NOthing to updated"},202)

    def user_login_model(self,data):
        self.cur.execute("select user_id ,name,email,phone,avatar,roll_id from users where email=%s and password=%s",(data["email"],data["password"]))
        result=self.cur.fetchall()
        userdata=result[0]
        exp_time=datetime.now()+timedelta(minutes=15)
        exp_epochtime=int(exp_time.timestamp())
        payload={
            "payload":userdata,
            "exp":exp_epochtime
        }
        token=jwt.encode(payload,"token",algorithm="HS256")
        return make_response({"token":token},200)   
