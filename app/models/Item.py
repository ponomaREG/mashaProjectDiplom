
from email.mime import image
import os
from sqlite3 import SQLITE_OK
import stat
from app.models.SqlExecuter import SqlExecuter
from config import BaseConfig

class Item:

    @staticmethod
    def createItem(
        name,
        number,
        book,
        author,
        date,
        place,
        size,
        picies,
        material,
        condition,
        era,
        hall,
        type,
        description,
        registration,
        image
    ):
        print(hall)
        eraId = Item.insertEraIfNotExist(era, "")
        imageId = Item.createImage(image)
        row = SqlExecuter.executeModif("INSERT INTO `museum`.`item` ( `book`, `number`, `registration`, `author`, `place`, `era`, `date`, `size`, `pieces`, `material`, `description`, `collection`, `hall`, `type`, `img`, `name`, `condition`, `status`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', NULL, '{}', '{}', '{}', '{}', '{}', '{}');".format(book, number, registration, author, place,eraId, date, size, picies, material, description, hall, type, imageId["data"], name,condition, "Есть"))
        return SqlExecuter.transformOneRow(row)

    @staticmethod
    def getItemsByBook(bookId):
        rows = SqlExecuter.getAllRowsPacked("SELECT * FROM item WHERE book = {};".format(bookId))
        images = {}
        for it in rows['data']:
            images[it['iditem']] = Item.__getImgPath(it['img'])
        rows['images'] = images
        return SqlExecuter.transformManyRow(rows)


    @staticmethod
    def getItemsByCollectionId(collectionId, isAll = True):
        result = {}
        if(isAll):
            rows = SqlExecuter.getAllRowsPacked("SELECT * FROM item where collection = {} ORDER BY iditem;".format(collectionId))
        else:
            rows = SqlExecuter.getAllRowsPacked("SELECT * FROM item where collection = {} and status != 'Списан' ORDER BY iditem;".format(collectionId))
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
                images[it['iditem']] = Item.__getImgPath(it['img'])
            result['images'] = images
        return result

    @staticmethod
    def getItemsByHall(hall, isAll = True):
        result = {}
        if(isAll):
            rows = SqlExecuter.getAllRowsPacked("SELECT * FROM item WHERE hall = {};".format(hall))
        else:
            rows = SqlExecuter.getAllRowsPacked("SELECT * FROM item WHERE hall = {} and status != 'Списан';".format(hall))
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
                images[it['iditem']] = Item.__getImgPath(it['img'])
            result['images'] = images
        return result

    @staticmethod
    def createImage(file):
        name = file.filename
        file.save(os.path.join(BaseConfig.PICS_DIR, name))
        row = SqlExecuter.executeModif("INSERT INTO `museum`.`image` (`itemimage`) VALUES ('{}');".format(name))
        return SqlExecuter.transformOneRow(row)

    @staticmethod
    def getItemByItemId(itemId, isAll = True):
        result = {}
        if(isAll):
            row = SqlExecuter.getOneRowsPacked("SELECT * FROM item where iditem = {};".format(itemId))
        else:
            row = SqlExecuter.getOneRowsPacked("SELECT * FROM item where iditem = {} and status != 'Списан';".format(itemId))
        if (row is None):
            result['data'] = {}
            result['status'] = 1
            result['message'] = "Empty result"
        else:
            result['message'] = 'OK'
            result['status'] = 0
            result['data'] = row
            result['image'] = Item.__getImgPath(row["img"])
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
    def insertEraIfNotExist(eraname, eradescription):
        exEra = Item.getEraByEraName(eraname)
        print(exEra)
        if exEra['status'] != 0:
            row = SqlExecuter.executeModif("INSERT INTO `museum`.`era` (`eraname`, `eradescription`) VALUES ('{}', '{}');".format(eraname, eradescription))
            return SqlExecuter.transformOneRow(row)["data"]
        return exEra["data"]["idera"]

    @staticmethod
    def getAllTypes():
        rows = SqlExecuter.getAllRowsPacked("SELECT * FROM type;")
        return SqlExecuter.transformManyRow(rows)

    @staticmethod
    def getFundByFundId(fundId):
        row = SqlExecuter.getOneRowsPacked("SELECT * FROM fund WHERE idfund = {};".format(fundId))
        return SqlExecuter.transformOneRow(row)

    @staticmethod
    def getEraByEraName(eraName):
        row = SqlExecuter.getOneRowsPacked("SELECT * FROM era where eraname = '{}';".format(eraName))
        return SqlExecuter.transformOneRow(row)

    @staticmethod
    def getItemType(typeId):
        row = SqlExecuter.getOneRowsPacked("SELECT * FROM type where idtype = {};".format(typeId))
        return SqlExecuter.transformOneRow(row)

    @staticmethod
    def getDistinctAuthor():
        row = SqlExecuter.getAllRowsPacked("SELECT DISTINCT author FROM item;")
        return SqlExecuter.transformManyRow(row)

    @staticmethod
    def getDistinctEra():
        row = SqlExecuter.getAllRowsPacked("SELECT DISTINCT eraname from era;")
        return SqlExecuter.transformManyRow(row)

    @staticmethod
    def getDistinctDate():
        rows = SqlExecuter.getAllRowsPacked("SELECT DISTINCT date from item;")
        return SqlExecuter.transformManyRow(rows)

    @staticmethod
    def getDistinctPlace():
        rows = SqlExecuter.getAllRowsPacked("SELECT DISTINCT place from item;")    
        return SqlExecuter.transformManyRow(rows)

    @staticmethod
    def __getImgPath(imgId):
        row = SqlExecuter.getOneRowsPacked("SELECT * FROM image WHERE idimage = {};".format(imgId))
        return row['itemimage']