from app.models.SqlExecuter import SqlExecuter


class Subscribe:


    @staticmethod
    def subscribeUser(user):
        result = {}
        if(user.dateend is None or user.datebegin is None):
            lrid = SqlExecuter.executeModif("insert subscriber(`uid`) values({});".format(user.userID))
            result['status'] = 0
            result['data'] = lrid
            return result
        else:
            lrid = SqlExecuter.executeModif('update subscriber set datebegin = CURRENT_TIMESTAMP where uid = {};'.format(user.userID))
            result['status'] = 10
            result['data'] = lrid
            return result
