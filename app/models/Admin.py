from app import db
from app.models.SqlExecuter import connection 
from app.admin.logger import AdminLogger as Logger




class Admin:

    @staticmethod
    def __executeAndGetAllRowsAndKeys(sqlQuery):
        cursor = connection.cursor()
        cursor.execute(sqlQuery)
        allRows = cursor.fetchall()
        columns_names = [i[0] for i in cursor.description]
        cursor.close()
        return {'data':allRows,'keys':columns_names}
    
    @staticmethod
    def __makeResultResponse(sqlQuery):
        res =  Admin.__executeAndGetAllRowsAndKeys(sqlQuery)
        if(len(res['data']) == 0):
            res['status'] = 3
            res['message'] = 'Empty'
            res['data'] = []
        else:
            res['status'] = 0
            res['message'] = 'OK'
        return res

    @staticmethod
    def getInfoOfUserBy(columnName,value):
        query = 'select * from user where {} like "%{}%";'.format(columnName,value)
        return Admin.__makeResultResponse(query)

    @staticmethod
    def getInfoOfPairBy(columnName,value):
        query = 'select * from pair where {} like "%{}%";'.format(columnName,value)
        return Admin.__makeResultResponse(query)

    @staticmethod
    def deleteRowFromTable(table,column,value):
        




    @staticmethod
    def getColumnsOfTable(tableName):
        return Admin.__makeResultResponse('SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_NAME`="{}";'.format(tableName))

   