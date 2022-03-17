from flask import jsonify, request, redirect, url_for, render_template, session
from app import app
from app import login_manager
from app.model import load_user
from app.models.Collection import Collection
from app.models.Item import Item
from app.model import User
from app.models.SqlExecuter import SqlExecuter
import flask_login
from werkzeug.utils import secure_filename
from utils.security import Security
from datetime import datetime,timedelta,timezone
from urllib.parse import unquote_to_bytes,parse_qsl
import os

    
@app.route("/",methods=['GET'])
def main():
    return render_template("main.html", user = flask_login.current_user)

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
            return redirect(url_for('main'))# Перекидываем на страницу книг
        else:
            return render_template('login.html',error = "Not found")#Выводим страницу логина с ошибкой
    else:
        return render_template('login.html')# Если метод обращения не POST , то выводим html страницу логина



@app.route('/logout',methods=['GET'])
@flask_login.login_required
def logoutUser():
    flask_login.logout_user()
    return redirect(url_for('main'))

#-------------------------------------------------------------------
#USER INFO BLOCK
#-------------------------------------------------------------------

@app.route('/user',methods=['GET'])
@flask_login.login_required # Пример декоратора
def userInfo():
        return render_template('user.html',user = flask_login.current_user)

#-------------------------------------------------------------------
#COLLECTION BLOCK
#-------------------------------------------------------------------

@app.route('/collections', methods = ["GET"])
def collectionsPage():
    result = Collection.getAllCollections()
    if(result["status"] == 0):
        return render_template('collections.html', data = result["data"],user = flask_login.current_user)
    else:
        return render_template('collections.html', error = result['message'],user = flask_login.current_user)

@app.route("/collection/<int:collectionId>")
def collectionDetailPage(collectionId):
    collection = Collection.getCollectionById(collectionId)
    items = Item.getItemsByCollectionId(collectionId)
    if (collection['status'] != 0 or items['status'] != 0):
        return render_template('collection.html', user = flask_login.current_user, error = items['message'])
    return render_template('collection.html', user = flask_login.current_user, collection = collection['data'], dataitem = items['data'], images = items['images'])

#-------------------------------------------------------------------
#ITEM BLOCK
#-------------------------------------------------------------------

@app.route("/item/<int:itemId>")
def itemDetailPage(itemId):
    item = Item.getItemByItemId(itemId)
    if (item['status'] == 0):
        collection = Collection.getCollectionById(item['data']['collection'])
        era = Item.getEraByEraId(item['data']['era'])
        return render_template("item.html", user = flask_login.current_user,item = item['data'], collection = collection['data'], era = era['data'], image = item['image'])
    else:
        return redirect(url_for("main"))

#-------------------------------------------------------------------
#HALL BLOCK
#-------------------------------------------------------------------

@app.route("/halls")
def hallsPage():
    return render_template("halls.html", user = flask_login.current_user)
    
@app.route("/halls/<string:hallName>")
def hallPage(hallName):
    result = Item.getItemsByHall(hallName)
    if (result['status'] != 0):
        return render_template("hall.html", user = flask_login.current_user, error = result['message'])
    return render_template("hall.html", user = flask_login.current_user, data = result['data'], images = result['images'], hallName = hallName)
    
#-------------------------------------------------------------------
#ERROR HANDLER BLOCK
#-------------------------------------------------------------------

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('main'))


@app.errorhandler(401)
def unauthorized(e):
    return redirect(url_for('loginUser'))