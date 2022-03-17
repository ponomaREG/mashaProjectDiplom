

from app.models.SqlExecuter import SqlExecuter


class Collection:

    @staticmethod
    def getAllCollections():
        result = {}
        rows = SqlExecuter.getAllRowsPacked("SELECT * FROM collection ORDER BY idcollection;")
        if(len(rows) == 0):
            result['data'] = []
            result['status'] = 1
            result['message'] = 'Empty result'
            return result
        else:    
            result['data'] = rows
            result['status'] = 0
            result['message'] = 'OK'
        return result

    @staticmethod
    def getCollectionById(collectionId):
        result = {}
        row = SqlExecuter.getOneRowsPacked("SELECT * FROM collection where idcollection = {};".format(collectionId))
        if (row is None):
            result['data'] = {}
            result["status"] = 1
            result['message'] = "Empty result"
        else:
            result['data'] = row
            result['status'] = 0
            result['message'] = 'OK'
        return result
                    