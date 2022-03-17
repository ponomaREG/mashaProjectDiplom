
from email.mime import image
import stat
from app.models.SqlExecuter import SqlExecuter

class Item:

    @staticmethod
    def getItemsByCollectionId(collectionId):
        result = {}
        rows = SqlExecuter.getAllRowsPacked("SELECT * FROM item where collection = {} ORDER BY iditem;".format(collectionId))
        if (rows is None):
            result['data'] = []
            result['status'] = 2
            result['message'] = "Unexpected error"
        elif(len(rows) == 0):
            result['data'] = []
            result['status'] = 1
            result['message'] = "Empty result"
        else:
            result['data'] = rows
            result['status'] = 0
            result['message'] = "OK"
            images = {}
            for it in result['data']:
                images[it['iditem']] = Item.__getImgPath(it['iditem'])
            result['images'] = images
        return result

    @staticmethod
    def getItemsByHall(hall):
        result = {}
        print("SELECT * FROM item WHERE hall = {};".format(hall))
        rows = SqlExecuter.getAllRowsPacked("SELECT * FROM item WHERE hall = {};".format(hall))
        if (rows is None):
            result['data'] = []
            result['status'] = 2
            result['message'] = "Unexpected error"
        elif(len(rows) == 0):
            result['data'] = []
            result['status'] = 1
            result['message'] = "Empty result"
        else:
            result['data'] = rows
            result['status'] = 0
            result['message'] = "OK"
            images = {}
            for it in result['data']:
                images[it['iditem']] = Item.__getImgPath(it['iditem'])
            result['images'] = images
        return result

    @staticmethod
    def getItemByItemId(itemId):
        result = {}
        row = SqlExecuter.getOneRowsPacked("SELECT * FROM item where iditem = {};".format(itemId))
        if (row is None):
            result['data'] = {}
            result['status'] = 1
            result['message'] = "Empty result"
        else:
            result['message'] = 'OK'
            result['status'] = 0
            result['data'] = row
            result['image'] = Item.__getImgPath(itemId)
        return result

    @staticmethod
    def getEraByEraId(eraId):
        result = {}
        row = SqlExecuter.getOneRowsPacked("SELECT * FROM era where idera = {};".format(eraId))
        if (row is None):
            result['message'] = 'Empty result'
            result['status'] = 1
            result['data'] = {}
        else:
            result['message'] = 'OK'
            result['status'] = 0
            result['data'] = row
        return result

    @staticmethod
    def __getImgPath(imgId):
        row = SqlExecuter.getOneRowsPacked("SELECT * FROM image WHERE idimage = {};".format(imgId))
        return row['itemimage']