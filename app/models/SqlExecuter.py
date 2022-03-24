import pymysql
from pymysql.cursors import DictCursor


connection = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = 'root',
    db = 'museum',
    charset = 'utf8',
    use_unicode = True,
    cursorclass = DictCursor
)



class SqlExecuter:

    @staticmethod
    def getOneRowAndColumns(query):
        cursor = connection.cursor()
        cursor.execute(query)
        row = cursor.fetchone()
        cursor.close()
        return row

    @staticmethod
    def getAllRowAndColumns(query):
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows


    @staticmethod
    def getAllRowsPacked(query):
        try:
            return SqlExecuter.getAllRowAndColumns(query)
        except:
            return None

    @staticmethod
    def getOneRowsPacked(query):
        try:
            return SqlExecuter.getOneRowAndColumns(query)
        except:
            return None

    
    @staticmethod
    def transformOneRow(row):
        result = {}
        if (row is None):
            result['message'] = 'Empty result'
            result['status'] = 2
            result['data'] = {}
        else:
            result['message'] = 'OK'
            result['status'] = 0
            result['data'] = row
        return result

    @staticmethod
    def transformManyRow(rows):
        result = {}
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



    @staticmethod
    def executeModif(query):
        cursor = connection.cursor()
        cursor.execute(query)
        lastrowid = cursor.lastrowid
        connection.commit()
        cursor.close()
        return lastrowid