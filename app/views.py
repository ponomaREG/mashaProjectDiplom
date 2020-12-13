from flask import jsonify, request, redirect, url_for, render_template
from app import app
from app import login_manager
from app.model import load_user
from app.models.User import User
from app.models.Product import Product
from app.models.Cart import Cart
from app.models.Order import Order
from app.models.Holland import Holland
from app.models.SqlExecuter import SqlExecuter
from app.admin.models import *
from app.admin.views import *
from utils import pageHelper
import flask_login
from utils import sqlQueryHelper, tagsHelper
from werkzeug.utils import secure_filename
from utils.security import Security
import os



@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('loginUser'))
    
    
# @app.route("/",methods=['GET'])
# def main():
#     return redirect(url_for('showBooksDefault'))

@app.route("/",methods=['GET'])
@flask_login.login_required
def main():
    if(flask_login.current_user.is_authenticated):
        user = flask_login.current_user
        return jsonify({"user":format("{} {}".format(user.first_name,user.last_name))})
    return redirect(url_for('loginUser'))


@app.route("/whatthefuck",methods=["GET"])
def what():
    data = SqlExecuter.getAllRowsPacked("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA='dating';")
    return jsonify({'data':data})
    

@app.route("/holland",methods=['GET'])
def hollandStartPage():
    return render_template("holland.html",user = flask_login.current_user)


@app.route("/holland/<int:number>")
def hollandQuiz(number):
    result = Holland.getWords(number)
    if(result['status'] == 0):
        return render_template("quiz.html",data=result['data'])
    else:
        return redirect(url_for('main'))


@app.route("/login",methods = ['GET','POST'])
def loginUser():
    if(flask_login.current_user.is_authenticated): #Проверяем вошел ли уже пользователь
        return redirect(url_for('main')) #Перекидываем на страницу профиля
    if(request.method == 'POST'): # Если метод обращения к url POST
        phone = Security.escape_sql(request.form.get('phone',type=str)) # Получаем введенный email 
        password = Security.escape_sql(request.form.get('password',type=str)) # Получаем введенный пароль
        userID = User.validateUserAndReturnUserID(phone,password) #Получаем ID пользователя по введенному email и паролю
        
        if(userID != -1):# Если пользователь найден
            flask_login.login_user(load_user(userID),remember=True)#Логиним пользователя в системе
            return redirect(url_for('hollandStartPage'))# Перекидываем на страницу книг
        else:
            return render_template('login.html',error = "Not found")#Выводим страницу логина с ошибкой
    else:
        return render_template('login.html')# Если метод обращения не POST , то выводим html страницу логина

@app.route('/registration',methods=['GET','POST'])
def registrationUser():
    if(flask_login.current_user.is_authenticated):
        return redirect(url_for('main'))
    if(request.method == 'POST'):
        phone = Security.escape_sql(request.form.get('phone',type=str)) # Получаем введенный email пользователя
        pswd = Security.escape_sql(request.form.get('pswd',type=str)) # Получаем введенный пароль пользователя
        pswd2 = Security.escape_sql(request.form.get('pswd2',type=str)) # Получаем введенный 2 пароль пользователя
        first_name = Security.escape_sql(request.form.get('firstName',type=str)) # Получаем введенныое имя пользователя
        last_name = Security.escape_sql(request.form.get('lastName',type=str)) # Получаем введенную фамилию пользователя
        birthdate = Security.escape_sql(request.form.get('birthDate'))# Получаем введенную дата рождения пользователя
        if(pswd != pswd2):
            return render_template('registration.html',error = 'Password mismatch') # Возвращаем html с ошибкой
        resultRegisterOperation = User.registerUser(phone,pswd,last_name,first_name,birthdate) # Создаем пользователя
        if(resultRegisterOperation["status"] == 8):
            return render_template('registration.html',error = 'User already exists') # Возвращаем html с ошибкой
        elif(resultRegisterOperation['status'] == 7):
            return render_template('registration.html',error = 'Incorrect email') # Возвращаем html с ошибкой
        flask_login.login_user(load_user(resultRegisterOperation["userID"]),remember=True) # Авторизируем пользователя
        return redirect(url_for('userInfo'))
    else:
        return render_template('registration.html')# Возвращаем html с формой


@app.route('/user',methods=['GET'])
@flask_login.login_required # Пример декоратора
def userInfo():
        return render_template('user-profile.html',user = flask_login.current_user)

@app.route('/logout',methods=['GET'])
@flask_login.login_required
def logoutUser():
    flask_login.logout_user()
    return redirect(url_for('main'))

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('main'))







