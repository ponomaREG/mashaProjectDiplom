

from app.models.SqlExecuter import SqlExecuter
from app.models.Item import Item


class Collection:

    @staticmethod
    def createCollection(
        name,
        description,
        theme,
        parametr
    ):
        collection = SqlExecuter.executeModif("INSERT INTO `museum`.`collection` (`collectionname`, `collectiondescription`) VALUES ('{}', '{}');".format(name, description))
        if(theme == 1):
            row = SqlExecuter.executeModif("UPDATE item SET collection = {} WHERE author = '{}';".format(collection, parametr))
        elif(theme == 2):
            era = Item.getEraByEraName(parametr)
            print("UPDATE item SET collection = {} WHERE era = {};".format(collection, era["data"]))
            row = SqlExecuter.executeModif("UPDATE item SET collection = {} WHERE era = {};".format(collection, era["data"]["idera"]))
        elif (theme == 3):
            row = SqlExecuter.executeModif("UPDATE item SET collection = {} WHERE date = '{}';".format(collection, parametr))
        else:
            row = SqlExecuter.executeModif("UPDATE item SET collection = {} WHERE place = '{}';".format(collection, parametr))
        return SqlExecuter.transformOneRow(row)

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
                    