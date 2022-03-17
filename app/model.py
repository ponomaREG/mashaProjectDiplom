from utils import md5helper
from app import login_manager
from flask_login import UserMixin
from app.models.User import *
from app.models.Collection import *
from utils.timeHelper import getTimeStampNow



@login_manager.user_loader
def load_user(userID):
    row = SqlExecuter.getOneRowsPacked('select * from user where iduser = {};'.format(userID))
    if(row is None):
        return None
    user = User(iduser = row['iduser'], mail = row['mail'],
    pass_hash = row['pass_hash'],lname=row['lname'],
    fname =row['fname'] ,phone=row['phone'], stuff = row['stuff'])
    return user
