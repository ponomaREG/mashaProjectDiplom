from app.models.SqlExecuter import SqlExecuter

class Museum:

    @staticmethod
    def getMesuemById(museumId):
        result = {}
        row = SqlExecuter.getOneRowsPacked("SELECT * FROM museum where idmuseum = {};".format(museumId))
        if (row is None):
            result['data'] = {}
            result['status'] = 1
            result['message'] = "Empty result"
        else:
            result['message'] = 'OK'
            result['status'] = 0
            result['data'] = row
        return result
        
    @staticmethod
    def getAllMuseumsWithKeys():
        result = {}
        row = SqlExecuter.getAllRowsPacked("SELECT * FROM museum;")
        if (row is None):
            result['data'] = {}
            result['status'] = 1
            result['message'] = "Empty result"
        else:
            result['message'] = 'OK'
            result['status'] = 0
            r = {}
            for m in row:
                r[m["idmuseum"]] = m
            result["data"] = r
        return result

    @staticmethod
    def getMuseumByItemId(itemId):
        row = SqlExecuter.getOneRowsPacked("SELECT museum.name FROM museum inner join book inner join item where item.iditem = {} and item.book = book.idbook and museum.idmuseum = book.museum;".format(itemId))
        return SqlExecuter.transformOneRow(row)