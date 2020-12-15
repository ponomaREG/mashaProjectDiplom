from app.models.SqlExecuter import SqlExecuter



class Pair:



    @staticmethod
    def getPairsOfUser(userID):
        response = {}
        data = SqlExecuter.getAllRowsPacked('select fname,lname,tel,bdate from pair inner join user where user.id = pair.user_id_2 and user_id_1 = {} order by pair.date desc;'.format(userID))
        if(len(data) == 0):
            response['status'] = 3
            response['data'] = []
        else:
            response['status'] = 0
            response['data'] = data
        return response

    @staticmethod
    def findNewPairsForUser(userID,code):
        correctUsersIdForMatch = []
        # potentMatchesQuery = "select * from result where user_id != {0} and code like '{1}%' and user_id not in (select user_id_1 from pair where user_id_2 = {0}) and user_id not in (select user_id_2 from pair where user_id_1 = {0}) order by id desc;".format(userID,code[0:2])
        # pMatches = SqlExecuter.getAllRowsPacked(potentMatchesQuery)
        query = "select * from result where user_id != {0} and code like '{1}%' and user_id not in (select user_id_1 from pair where user_id_2 = {0}) and user_id not in (select user_id_2 from pair where user_id_1 = {0}) order by id desc;".format(userID,code[0:2])
        data = SqlExecuter.getAllRowsPacked(query)
        uniqueID = []
        for row in data:
            uniqueID.append(row['user_id'])
        uniqueID = list(set(uniqueID))
        print(uniqueID)
        for id in uniqueID:
            lastResultOfUser = SqlExecuter.getOneRowsPacked("select * from result where user_id = {} order by id desc LIMIT 1;".format(id))
            print(lastResultOfUser)
            if(lastResultOfUser['code'][0:2] == code[0:2]):
                correctUsersIdForMatch.append(id)
        for correctId in correctUsersIdForMatch:
            SqlExecuter.executeModif("insert into pair(`user_id_1`,`user_id_2`) values({},{});".format(userID,correctId))
            SqlExecuter.executeModif("insert into pair(`user_id_1`,`user_id_2`) values({},{});".format(correctId,userID))
        

        