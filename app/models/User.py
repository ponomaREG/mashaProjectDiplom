from flask_login import UserMixin
from utils import md5helper
from app.models.SqlExecuter import SqlExecuter


class User(UserMixin):
    iduser = -1
    fname = None
    lname = None
    mail = None
    pass_hash = None
    phone = None
    stuff = None

    def __init__(self,iduser, fname, lname, mail, pass_hash, phone, stuff):
        self.iduser = iduser
        self.fname = fname
        self.lname = lname
        self.mail = mail
        self.pass_hash = pass_hash
        self.phone = phone
        self.stuff = stuff

    def get_id(self):
        return str(self.iduser)
    
    
    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

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
            'select * from user where phone \
             = "{}" and pass_hash = "{}"'.format(phone,md5helper.ecnrypt(password))
            )
        return row is not None

    @staticmethod
    def validateUserAndReturnUserID(phone,password):
        row = SqlExecuter.getOneRowsPacked(
            'select * from user where phone \
             = "{}" and pass_hash = "{}"'.format(phone,md5helper.ecnrypt(password))
            )
        if(row is None):
            return -1
        else:
            return row['iduser'] # Возвращаем ID пользователя