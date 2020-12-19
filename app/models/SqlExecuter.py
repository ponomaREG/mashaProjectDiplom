import pymysql
from pymysql.cursors import DictCursor


connection = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = 'Huyhuyhuy123',
    db = 'dating',
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
    def executeModif(query):
        cursor = connection.cursor()
        cursor.execute(query)
        lastrowid = cursor.lastrowid
        connection.commit()
        cursor.close()
        return lastrowid