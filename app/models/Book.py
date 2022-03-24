from app.models.SqlExecuter import SqlExecuter

class Book:

    @staticmethod
    def putBook(number, type, date, museum):
        result = {}
        row = SqlExecuter.executeModif("INSERT INTO `museum`.`book` (`type`, `date`, `museum`, `number`) VALUES ('{}', '{}', '{}', '{}');".format(type, date, museum, number))
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
    def getBookDetail(bookId):
        result = {}
        row = SqlExecuter.getOneRowsPacked("SELECT * FROM book where idbook = {};".format(bookId))
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
    def getAllBooks():
        result = {}
        rows = SqlExecuter.getAllRowsPacked("SELECT * FROM book ORDER BY idbook;")
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
        return result

