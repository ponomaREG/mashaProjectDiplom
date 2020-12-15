from utils import md5helper
from app import login_manager
from flask_login import UserMixin
from app.models.User import *
from utils.timeHelper import getTimeStampNow



@login_manager.user_loader
def load_user(userID):
    row = SqlExecuter.getOneRowsPacked('select * from user where id = {};'.format(userID))
    if(row is None):
        return None
    user = User(userID = row['id'],email = row['mail'],
    password_hash = row['pass_hash'],last_name=row['lname'],
    first_name =row['fname'] ,birthdate = row['bdate'],phone=row['tel'])

    if checkIfUserSubscriber(userID):
        user.set_isSubscriber(True)
        date_begin,date_end = User.getSubInfo(row['id'])
        user.datebegin = date_begin
        user.dateend = date_end
    if(checkIfUserAdmin(userID)):
        user.set_admin(True)
    return user


def checkIfUserSubscriber(userID):
    if(SqlExecuter.getOneRowsPacked("select * from subscriber where uid = {} and date_end>'{}';".format(userID,getTimeStampNow())) is None):
        if(SqlExecuter.getOneRowsPacked('select * from subscriber where uid = {}'.format(userID)) is not None):
            SqlExecuter.executeModif('delete from subscriber where uid={}'.format(userID))
        return False
    return True

def checkIfUserAdmin(userID):
    return SqlExecuter.getOneRowsPacked('select * from stuff where user_id = {};'.format(userID)) is not None
