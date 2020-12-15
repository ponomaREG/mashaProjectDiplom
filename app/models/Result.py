from app.models.SqlExecuter import SqlExecuter




class Result:


    @staticmethod
    def insertResult(code,userID):
        response = {}
        lid = SqlExecuter.executeModif('insert into result(`code`,`user_id`) values("{}",{});'.format(code,userID))
        if(lid > -1):
            response['status'] = 0
            response['data'] = lid
        else:
            response['status'] = 5
            response['data'] = -1

        return response

    @staticmethod
    def getOneResultOfUser(userID):
        response = {}
        data = SqlExecuter.getOneRowsPacked('select code,date from result where user_id = {} order by id desc;'.format(userID))
        if(data is None):
            response['status'] = 3
            response['data'] = []
        else:
            response['status'] = 0
            response['data'] = [data]
        return response

    @staticmethod
    def getAllResultsOfUser(userID):
        response = {}
        data = SqlExecuter.getAllRowsPacked("select code,date from result where user_id = {} order by id desc;".format(userID))
        if(len(data) == 0):
            response['status'] = 3
            response['data'] = []
        else:
            response['status'] = 0
            response['data'] = data
        return response