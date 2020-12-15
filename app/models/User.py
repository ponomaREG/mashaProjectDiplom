from flask_login import UserMixin
from app import db
from app.models.Cart import Cart
from utils import md5helper
from utils import validationForm
from app.models.SqlExecuter import SqlExecuter


class User(UserMixin):
    userID = -1
    first_name = None
    last_name = None
    birthdate = None
    email = None
    password_hash = None
    is_admin = False
    is_subscriber = False
    datebegin = None
    dateend = None
    phone = None

    def __init__(self,userID,email,password_hash,last_name,first_name,birthdate,phone):
        self.userID = userID
        self.email = email
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate
        self.phone = phone
    

    def is_active(self):
        return True
    
    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def set_admin(self,boolean):
        self.is_admin = boolean
    
    def set_isSubscriber(self,boolean):
        self.is_subscriber = boolean

    def isSubscriber(self):
        return self.is_subscriber

    def get_id(self):
        return str(self.userID)

    def getTotalCostOfCart(self):
        return Cart.countTotalCostOfUser(self.userID)

    def getCountOfItemsInCart(self):
        return Cart.getCountOfItemsInCart(self.userID)["data"][0]

    def getUserMarkTo(self,productID):
        row = SqlExecuter.getOneRowsPacked('select mark from Рейтинг where user_id = {} and product_id = {};'.format(self.userID,productID))
        if(row is None):
            return None
        else:
            return float(row['mark'])


    @staticmethod
    def registerUser(phone,password,last_name,first_name,birthdate):
        result = {}
        row = SqlExecuter.getOneRowsPacked('select * from user where tel="{}";'.format(phone))
        if(row is not None):# Проверка,если пользователь с таким email существует
            result['status'] = 8
            result['message'] = 'User with same phone already exists' 
            return result
        # if(not validationForm.validationEmail(email)):# Если неправильно введен email
        #     result['status'] = 7
        #     result['message'] = 'Incorrect email'
        #     return result

        lastrowid = SqlExecuter.executeModif(
            'insert into user(`tel`,`lname`,`fname`,`bdate`,`pass_hash`) \
                values("{}","{}","{}","{}","{}")'.format(
                    phone,last_name,first_name,birthdate,md5helper.ecnrypt(password))
                )
        result["status"] = 0
        result["message"] = "OK"
        result["userID"] = lastrowid
        return result
        


    @staticmethod
    def getSubInfo(userID):
        row = SqlExecuter.getOneRowsPacked('select * from subscriber where uid = {};'.format(userID))
        if(row is not None):
            return (row['date_begin'],row['date_end'])

    
    @staticmethod
    def getInfo(value,column='id'):
        result = {}
        row = SqlExecuter.getOneRowsPacked('select * from user where {} = {};'.format(column,value))
        if(row is None):
            result['data'] = {}
            result['status'] = 1
            result['message'] = 'User not found'
            return result
        result['data'] = row
        result['status'] = 0
        result['message'] = 'OK'
        return result


    #LEGACY
    @staticmethod
    def addUser(data):
        result = {}
        try:
            last_name = data['last_name']
            first_name = data['first_name']
            password = data['password']
            birthdate = data['birthdate']
            email = data['email']
            tel = data['phone']
        except KeyError:
            result['status'] = 6
            result['message'] = 'Required field is missing'
            return result
        try:
            SqlExecuter.executeModif(
                'insert into user values("{}","{}",NULL,"{}","{}","{}");'.format(
                    last_name,first_name,
                    email,birthdate,
                    md5helper.ecnrypt(password)
                ))
        except Exception:
            result['status'] = 1
            result['message'] = 'SQL runtime error'
            return result
        result['status'] = 0
        result['message'] = 'OK'
        return result
    
    @staticmethod
    def validateUser(phone,password):
        row = SqlExecuter.getOneRowsPacked(
            'select * from user where tel \
             = "{}" and pass_hash = "{}"'.format(phone,md5helper.ecnrypt(password))
            )
        return row is not None

    @staticmethod
    def validateUserAndReturnUserID(phone,password):
        row = SqlExecuter.getOneRowsPacked(
            'select * from user where tel \
             = "{}" and pass_hash = "{}"'.format(phone,md5helper.ecnrypt(password))
            )
        if(row is None):
            return -1
        else:
            return row['id'] # Возвращаем ID пользователя