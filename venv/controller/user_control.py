from app import app
from model.user_model import user1
from model.auth_model import auth_model
from flask import request,send_file
from datetime import datetime

obj=user1()
auth=auth_model()

@app.route("/home")
@auth.token_model("/home")
def home():
    return obj.user_getall()

@app.route("/insert",methods=["POST"])
def addone():
    return obj.user_setall(request.args)
@app.route("/update",methods=["PUT"])
def update():
    return obj.user_updateall(request.form)

@app.route("/delete",methods=["DELETE"])
def delete():
    return obj.user_deleteall(request.form)
@app.route("/home/limit/<limit>/page/<page>",methods=["GET"])
def pagination(limit,page):
    return obj.user_pagination(limit,page)
@app.route("/home/<uid>/upload/avatar",methods=["PUT"])
def user_upload_controller(uid):
    file=request.files['Avatar']
    uniquefilename=str(datetime.now().timestamp()).replace(".","")
    filenamesplit=file.filename.split(".")
    ext=filenamesplit[-1]
    filepath=f"uploads/{uniquefilename}.{ext}"
    file.save(filepath)
    return obj.user_upload_model(uid,filepath)
@app.route("/uploads/<filename>")
def user_getavatar_control(filename):
    return send_file(f"uploads/{filename}")

@app.route("/home/login",methods=["POST"])
def user_login():
    return obj.user_login_model(request.form)