from distutils.command.config import config
import os
from random import random
from app.models.SqlExecuter import SqlExecuter
from dateutil.parser import parse
from config import BaseConfig
from docxtpl import DocxTemplate

class WriteOff:

    @staticmethod
    def createWriteOff(itemId, date, reason, picies, user, act):
        row = SqlExecuter.executeModif("INSERT INTO `museum`.`writeoff` (`reason`, `date`, `item`, `pieces`, `user`, `act`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}');".format(reason, date, itemId, picies, user, act))
        upd = SqlExecuter.executeModif("UPDATE item SET status = 'Списан' WHERE iditem = {};".format(itemId))
        return SqlExecuter.transformOneRow(row)

    @staticmethod
    def getWriteOffs():
        rows = SqlExecuter.getAllRowsPacked("SELECT * FROM writeoff;")
        return SqlExecuter.transformManyRow(rows)

    @staticmethod
    def generateAct(museum, picies, reason, date, actId):
        d = parse(date)
        context = {
            "museum" : museum,
            "picies" : picies,
            "reason" : reason,
            "day" : d.day,
            "month" : d.month,
            "year" : d.year,
            "act" : actId
        }
        doc = DocxTemplate(BaseConfig.DEFAULT_WORD_FILE)
        doc.render(context)
        path = os.path.join(BaseConfig.DEFAULT_WORD_DIR, "{}.docx".format(actId))
        doc.save(path)
        return ["/static/acts/{}.docx".format(actId), "{}.docx".format(actId)]

