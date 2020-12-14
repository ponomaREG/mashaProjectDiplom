
from app.models.SqlExecuter import SqlExecuter


class Holland:

    @staticmethod
    def getKeys():
        return ["Р","А","И","С","П","К","previously_pair"]


    @staticmethod
    def getWords(number):
        response = {}
        data = SqlExecuter.getOneRowsPacked("select id,word1,word2,answer.letter as 'letter1',answer2.letter as 'letter2' from quiz inner join answer inner join answer as answer2 where quiz.word1 = answer.word and quiz.word2 = answer2.word and id = {};".format(number))
        if(data is None):
            response['status'] = 3
            response['message'] = "EMPTY"
            response['data'] = {}
        else:
            response['data'] = data
            response['status'] = 0
            response['message'] = "OK"
        return response


    @staticmethod
    def getCountOfPairs():
        data = SqlExecuter.getOneRowsPacked("select count(*) as 'count' from quiz;")
        return data["count"]


    @staticmethod
    def sortDictByValues(dict):
        list_d = list(dict.items())
        list_d.sort(key=lambda i: i[1])
        list_d.reverse()
        return list_d
