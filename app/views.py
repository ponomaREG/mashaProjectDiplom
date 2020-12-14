from flask import jsonify, request, redirect, url_for, render_template, session
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


@app.route("/holland",methods=['GET'])
def hollandStartPage():
    clearSession(Holland.getKeys())
    setKeysSession(Holland.getKeys())
    return render_template("holland.html",user = flask_login.current_user)


@app.route("/holland/result",methods=["GET"])
def hollandResult():
    if(not checkKeysInSession(Holland.getKeys())):
        return redirect(url_for("hollandStartPage"))
    values = getValuesFromSession(Holland.getKeys())
    values.pop("previously_pair")
    valuesSort = Holland.sortDictByValues(values)
    return str(valuesSort)

    

@app.route("/holland/<int:number>",methods=["GET","POST"])
def hollandQuiz(number):
    print(session)
    if((not checkKeysInSession(Holland.getKeys())) or (session.get('previously_pair') + 1 != number)):
        return redirect(url_for("hollandStartPage"))
    if(request.method == "GET"):
        countOfPairs = Holland.getCountOfPairs()
        if(number > countOfPairs):
            resultOfQuiz = {}
            for key in Holland.getKeys():
                resultOfQuiz[key] = session[key]
            return redirect(url_for("hollandResult"))
        if(number == 1):
            session['countOfPairs'] = countOfPairs
        result = Holland.getWords(number)
        if(result['status'] == 0):
            return render_template("quiz.html",data=result['data'])
        else:
            return redirect(url_for('main'))
    else:
        if("word1" in request.form):
            letter = request.form.get("word1")
        elif("word2" in request.form):
            letter = request.form.get("word2")
        else:
            return redirect(url_for("hollandStartPage"))
        session[letter] = session.get(letter) + 1
        session['previously_pair'] = number
        return redirect(url_for("hollandQuiz",number=number+1))


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


@app.route("/counter",methods=["GET"])
def counter():
    if("visits" in session):
        session["visits"] = session.get("visits") + 1
        
    else:
        session["visits"] = 1
    return "<h1>Counter:{}</h1>".format(session.get("visits"))


def clearSession(keys):
    for key in keys:
        if(key in session):
            session.pop(key)

def setKeysSession(keys):
    for key in keys:
        session[key] = 0

def checkKeysInSession(keys):
    for key in keys:
        if(key not in session):
            return False
    return True

def getValuesFromSession(keys):
    resultOfQuiz = {}
    for key in Holland.getKeys():
                resultOfQuiz[key] = session[key]
    return resultOfQuiz










