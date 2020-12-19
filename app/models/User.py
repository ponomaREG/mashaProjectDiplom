from flask_login import UserMixin
from utils import md5helper
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


    @staticmethod
    def registerUser(phone,password,last_name,first_name,birthdate):
        result = {}
        row = SqlExecuter.getOneRowsPacked('select * from user where tel="{}";'.format(phone))
        if(row is not None):# Проверка,если пользователь с таким email существует
            result['status'] = 8
            result['message'] = 'User with same phone already exists' 
            return result

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