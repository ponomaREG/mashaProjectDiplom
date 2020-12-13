from app import db
from utils import md5helper, sqlQueryHelper, dateHelper
from app import login_manager
from flask_login import UserMixin
from app.models.User import *



@login_manager.user_loader
def load_user(userID):
    row = SqlExecuter.getOneRowsPacked('select * from user where id = {};'.format(userID))
    if(row is None):
        return None
    user = User(userID = row['id'],email = row['mail'],
    password_hash = row['pass_hash'],last_name=row['lname'],
    first_name =row['fname'] ,birthdate = row['bdate'],phone=row['tel'])
    # if(checkIfUserAdmin(userID)):
    #     user.set_level_of_access(getLevelOfAccess(userID))
    #     user.set_admin(True)
    return user



def checkIfUserAdmin(userID):
    return SqlExecuter.getOneRowsPacked('select * from Админ where user_id = {};'.format(userID)) is not None

def getLevelOfAccess(userID):
    if(checkIfUserAdmin(userID)):
        row = SqlExecuter.getOneRowsPacked('select * from Админ where user_id = {};'.format(userID))
        return int(row['level_of_access'])