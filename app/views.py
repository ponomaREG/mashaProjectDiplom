import imp
from xmlrpc.client import boolean
from flask import jsonify, request, redirect, url_for, render_template, session, send_file
from app import app
from app import login_manager
from app.model import load_user
from app.models.Collection import Collection
from app.models.Item import Item
from app.models.Book import Book
from app.models.Museum import Museum
from app.models.WriteOff import WriteOff
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
    items = Item.getItemsByCollectionId(collectionId, False)
    if (collection['status'] != 0 or items['status'] != 0):
        return render_template('collection.html', user = flask_login.current_user, error = items['message'])
    return render_template('collection.html', user = flask_login.current_user, collection = collection['data'], dataitem = items['data'], images = items['images'])

@app.route("/collection/create", methods = ["GET", "POST"])
def collectionCreatePage():
    if request.method == "POST":
        collectionName = Security.escape_sql(request.form.get("collectionName", type = str))
        collectionDescription = Security.escape_sql(request.form.get("collectionDescription", type = str))
        collectionTheme = request.form.get("theme", type = int)
        collectionParametr = Security.escape_sql(request.form.get("parametr", type = str))
        res = Collection.createCollection(
            collectionName,
            collectionDescription,
            collectionTheme,
            collectionParametr
        )
        if (res["status"] == 0):
            return redirect(url_for("collectionsPage"))
        else:
            authors = Item.getDistinctAuthor()
            places = Item.getDistinctPlace()
            era = Item.getDistinctEra()
            dates = Item.getDistinctDate()
            return render_template("collectioncreate.html", user = flask_login.current_user, authors = authors["data"], places = places["data"], era = era["data"], dates = dates["data"], error = res["message"])
    else:
        authors = Item.getDistinctAuthor()
        places = Item.getDistinctPlace()
        era = Item.getDistinctEra()
        dates = Item.getDistinctDate()
        return render_template("collectioncreate.html", user = flask_login.current_user, authors = authors["data"], places = places["data"], era = era["data"], dates = dates["data"])


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

# @app.route("/item/fill", methods=["GET", "POST"])
# def itemDetailPage(itemId):

@app.route("/item/<int:itemId>/stuff")
@flask_login.login_required
def itemStuffPage(itemId):
    item = Item.getItemByItemId(itemId)
    if (item['status'] == 0):
        collection = Collection.getCollectionById(item['data']['collection'])
        era = Item.getEraByEraId(item['data']['era'])
        return render_template("item.html", user = flask_login.current_user,item = item['data'], collection = collection['data'], era = era['data'], image = item['image'])
    else:
        return redirect(url_for("main"))

@app.route("/item/fill", methods = ["GET", "POST"])
def itemFillPage():
    books = Book.getAllBooks()
    types = Item.getAllTypes()
    if request.method == "POST":
        registration = Security.escape_sql(request.form.get("registration", type = str))
        name = Security.escape_sql(request.form.get("name", type = str))
        number = Security.escape_sql(request.form.get("number", type = str))
        book = request.form.get("book", type = int)
        author = Security.escape_sql(request.form.get("author", type = str))
        date = Security.escape_sql(request.form.get("date", type = str))
        place = Security.escape_sql(request.form.get("place", type = str))
        size = Security.escape_sql(request.form.get("size", type = str))
        picies = request.form.get("picies", type = int)
        material = Security.escape_sql(request.form.get("material", type = str))
        condition = Security.escape_sql(request.form.get("condition", type = str))
        era = Security.escape_sql(request.form.get("era", type = str))
        hall = Security.escape_sql(request.form.get("hall", type = str))
        type = request.form.get("type", type = int)
        description = Security.escape_sql(request.form.get("description", type = str))
        image = request.files["img"]
        r = Item.createItem(
            name,
            number,
            book,
            author,
            date,
            place,
            size,
            picies,
            material,
            condition,
            era,
            hall,
            type,
            description,
            registration,
            image
        )
        if(r["status"] == 0):
            return redirect(url_for("itemStuffPage", itemId = r["data"]))
        else:
            return render_template("itemfill.html", user= flask_login.current_user, error = r["message"], books = books["data"], types = types["data"])
    else:
        return render_template("itemfill.html", user = flask_login.current_user, books = books["data"], types = types["data"])

    

#-------------------------------------------------------------------
#HALL BLOCK
#-------------------------------------------------------------------

@app.route("/halls")
def hallsPage():
    return render_template("halls.html", user = flask_login.current_user)
    
@app.route("/halls/<string:hallName>")
def hallPage(hallName):
    result = Item.getItemsByHall(hallName, False)
    if (result['status'] != 0):
        return render_template("hall.html", user = flask_login.current_user, error = result['message'])
    return render_template("hall.html", user = flask_login.current_user, data = result['data'], images = result['images'], hallName = hallName)

    
#-------------------------------------------------------------------
#BOOK BLOCK
#-------------------------------------------------------------------

@app.route("/books")
@flask_login.login_required
def booksPage():
    result = Book.getAllBooks()
    museum = Museum.getAllMuseumsWithKeys()
    if(result['status'] == 0):
        return render_template('books.html', user = flask_login.current_user, data = result['data'], museums = museum["data"])
    else:
        return render_template('books.html', user = flask_login.current_user, error = result['message'])


@app.route("/books/<int:idBook>")
@flask_login.login_required
def bookDetailPage(idBook):
    result = Book.getBookDetail(idBook)
    if(result['status'] == 0):
        museum = Museum.getMesuemById(result['data']['museum'])
        return render_template('book.html', user = flask_login.current_user, book = result['data'], museum = museum["data"])
    else:
        return render_template('book.html', user = flask_login.current_user, error = result['message'], book = None)

@app.route("/books/fill", methods = ["GET", "POST"])
@flask_login.login_required
def bookFillPage():
    allMuseums = Museum.getAllMuseumsWithKeys()
    if request.method == "POST":
        number = Security.escape_sql(request.form.get("number", type=str))
        type = Security.escape_sql(request.form.get("type", type=str))
        date = Security.escape_sql(request.form.get("date", type=str))
        museum = request.form.get("museum", type=int)
        r = Book.putBook(number, type, date, museum)
        if (r['status'] == 0):
            return redirect(url_for('booksPage'))
        else:
            return render_template("bookfill.html", user = flask_login.current_user, error = r['message'], museums = allMuseums['data'])
    else:
        return render_template("bookfill.html", user = flask_login.current_user, museums = allMuseums['data'])


#-------------------------------------------------------------------
#WRITEOFF BLOCK
#-------------------------------------------------------------------

@app.route("/writeoff", methods = ["GET", "POST"])
@flask_login.login_required
def writeOffPage():
    if (request.method == "POST"):
        date = Security.escape_sql(request.form.get("date", type = str))
        item = request.form.get("item", type = int)
        reason = Security.escape_sql(request.form.get("reason", type = str))
        picies = request.form.get("picies", type = int)
        isGenerateAct = request.form.get("isGenerateAct", type = boolean)
        r = WriteOff.createWriteOff(item, date, reason, picies, flask_login.current_user.get_id(), "Не что тут")
        if r["status"] != 0:
            return render_template("writeoff.html", user = flask_login.current_user, error = r["message"])
        else:
            if isGenerateAct:
                museum = Museum.getMuseumByItemId(item)
                return redirect(url_for("generateAct", date = date, picies = picies, act = r["data"], reason = reason, museum = museum["data"]["name"]))
            return redirect(url_for("writeOffTabPage"))
    else:
        return render_template("writeoff.html", user = flask_login.current_user)

@app.route("/writeofftab")
@flask_login.login_required
def writeOffTabPage():
    writeOffs = WriteOff.getWriteOffs()
    if(writeOffs["status"] == 0):
        return render_template("writeofftab.html", user = flask_login.current_user, writeoffs = writeOffs["data"])
    else:
        return render_template("writeofftab.html", user = flask_login.current_user, error = writeOffs["message"], writeoffs = [])

@app.route("/act", methods = ["GET"])
def generateAct():
    museum = request.args.get("museum")
    date = request.args.get("date")
    picies = request.args.get("picies")
    actId = request.args.get("act")
    reason = request.args.get("reason")
    r = WriteOff.generateAct(museum, picies, reason, date, actId)
    return render_template("act.html", fileUrl = r[0], fileName = r[1])


#-------------------------------------------------------------------
#ERROR HANDLER BLOCK
#-------------------------------------------------------------------

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('main'))


@app.errorhandler(401)
def unauthorized(e):
    return redirect(url_for('loginUser'))