from flask import jsonify, request, redirect, url_for, render_template, session
from app import app
from app import login_manager
from app.model import load_user
from app.models.User import User
from app.models.Holland import Holland
from app.models.SqlExecuter import SqlExecuter
from app.models.Subscribe import Subscribe
from app.models.Admin import Admin
from app.models.Result import Result
from app.models.Pair import Pair
import flask_login
from werkzeug.utils import secure_filename
from utils.security import Security
from datetime import datetime,timedelta,timezone
from urllib.parse import unquote_to_bytes,parse_qsl
import os



@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('loginUser'))

def parse(query_string):
    return dict(parse_qsl(query_string, errors='ignore')), unquote_to_bytes(query_string)

@app.route('/api/authorize', methods=['GET'])
def authorize():
    args, decoded = parse(request.query_string)
    command = args.get(b'cmd')
    if not command:
        return {'error': 'No command specified'}, 400
    if command != b'ls':
        return {'error': 'Insufficient privileges'}, 403
    expiry = int((datetime.now(timezone.utc) + timedelta(seconds=15)).timestamp())
    expiry_arg = b'expiry=' + str(expiry).encode() + b'&'
    print(expiry_arg+decoded)
    return {'data':expiry_arg+decoded}
    
    
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


#-------------------------------------------------------------------
#QUIZ BLOCK
#-------------------------------------------------------------------

@app.route("/holland",methods=['GET'])
def hollandStartPage():
    clearSession(Holland.getKeys())
    setKeysSession(Holland.getKeys())
    return render_template("holland.html",user = flask_login.current_user)


@app.route("/holland/result",methods=["GET"])
@flask_login.login_required
def hollandResult():
    if(not checkKeysInSession(Holland.getKeys())):
        return redirect(url_for("hollandStartPage"))
    values = getValuesFromSession(Holland.getKeys())
    values.pop("previously_pair")
    valuesSort = Holland.sortDictByValues(values)
    code = ""
    for vals in valuesSort:
        code += vals[0]
    Result.insertResult(code,flask_login.current_user.userID)
    Pair.findNewPairsForUser(flask_login.current_user.userID,code)
    return redirect(url_for('userResults'))

    

@app.route("/holland/<int:number>",methods=["GET","POST"])
@flask_login.login_required
def hollandQuiz(number):
    if((not checkKeysInSession(Holland.getKeys())) or (session.get('previously_pair') + 1 != number)):
        return redirect(url_for("hollandStartPage"))
    if(request.method == "GET"):
        if('countOfPairs' in session):
            countOfPairs = int(session.get('countOfPairs'))
        else:
            countOfPairs = Holland.getCountOfPairs()
        if(number > countOfPairs):
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



#-------------------------------------------------------------------
#AUTH BLOCK
#-------------------------------------------------------------------

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
        flask_login.login_user(load_user(resultRegisterOperation["userID"]),remember=True) # Авторизируем пользователя
        return redirect(url_for('userInfo'))
    else:
        return render_template('registration.html')# Возвращаем html с формой



#-------------------------------------------------------------------
#USER INFO BLOCK
#-------------------------------------------------------------------

@app.route('/user',methods=['GET'])
@flask_login.login_required # Пример декоратора
def userInfo():
        return render_template('user.html',user = flask_login.current_user)


@app.route('/user/results',methods=['GET'])
@flask_login.login_required
def userResults():
    if(flask_login.current_user.is_subscriber):
        result = Result.getAllResultsOfUser(flask_login.current_user.userID)
    else:
        result = Result.getOneResultOfUser(flask_login.current_user.userID)
    if(result['status'] == 0):
        return render_template('results.html',data=result['data'])
    elif(result['status'] == 3):
        return render_template('results.html',data=result['data'])
    else:
        return redirect(url_for('userInfo'))


@app.route("/user/pairs",methods=['GET'])
@flask_login.login_required
def userPairs():
    result = Pair.getPairsOfUser(flask_login.current_user.userID)
    if(result['status'] == 0):
        return render_template('pairs.html',pairs = result['data'])
    elif(result['status'] == 3):
        return render_template('pairs.html',pairs = result['data'])



#-------------------------------------------------------------------
#SUB BLOCK
#-------------------------------------------------------------------



@app.route('/sub',methods=['GET'])
@flask_login.login_required
def subscribeUser():
    user = flask_login.current_user
    if(user.is_subscriber):
        return redirect(url_for("userInfo"))
    Subscribe.subscribeUser(user)
    return redirect(url_for('userInfo'))


#-------------------------------------------------------------------
#ADMIN BLOCK
#-------------------------------------------------------------------


@app.route('/admin',methods=['GET','POST'])
@flask_login.login_required
def adminPage():
    if(flask_login.current_user.is_admin):
        columnNamesUsers = Admin.getColumnsOfTable('user')
        columnNamesPairs = Admin.getColumnsOfTable('pair')
        if(request.method == "GET"):
            return render_template('admin-page.html',columnNamesUsers = columnNamesUsers['data'],columnNamesPairs = columnNamesPairs['data'])
        else:
             method = request.form.get('method',type=int)

             if(method == 1):
                column = request.form.get('column-user')
                value = request.form.get('value-user')
                resultOfResponseToDB = Admin.getInfoOfUserBy(column,value)
             elif(method == 2):
                column = request.form.get('column-pair')
                value = request.form.get('value-pair')
                resultOfResponseToDB = Admin.getInfoOfPairBy(column,value)
             elif(method == 3):
                 userID = request.form.get('userID',type=int)
                 resultOfResponseToDB = Admin.deleteRowFromTable('user','id',userID)
             elif(method == 4):
                 userID1 = request.form.get('userID1',type=int)
                 userID2 = request.form.get('userID2',type=int)
                 resultOfResponseToDB = Admin.deleteRowFromTableByWhere('pair',{'user_id_1':userID1,'user_id_2':userID2})
                 Admin.deleteRowFromTableByWhere('pair',{'user_id_1':userID2,'user_id_2':userID1})
             return render_template('admin-page.html',columnNamesUsers = columnNamesUsers['data'],columnNamesPairs = columnNamesPairs['data'],resultOfResponse = resultOfResponseToDB)

    else:
        return redirect(url_for('hollandStartPage'))

@app.route('/logout',methods=['GET'])
@flask_login.login_required
def logoutUser():
    flask_login.logout_user()
    return redirect(url_for('main'))

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('main'))



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










