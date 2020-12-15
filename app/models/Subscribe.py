from app.models.SqlExecuter import SqlExecuter
from utils.timeHelper import getTimeStampWithOffsetMinutes


class Subscribe:


    @staticmethod
    def subscribeUser(user):
        result = {}
        if(user.dateend is None or user.datebegin is None):
            lrid = SqlExecuter.executeModif("insert subscriber(`uid`,`date_end`) values({},'{}');".format(user.userID,getTimeStampWithOffsetMinutes(1))) #TODO: CHANGE METHOD
            result['status'] = 0
            result['data'] = lrid
            return result
        else:
            # futureTimestamp = getTimeStampWithOffsetMinutes(1)
            # lrid = SqlExecuter.executeModif('update subscriber set date_begin = CURRENT_TIMESTAMP and date_end = "{}"  where uid = {};'.format(futureTimestamp,user.userID))
            result['status'] = 10
            # result['data'] = lrid
            return result
