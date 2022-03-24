import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(50)
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    DEFAULT_WORD_FILE = os.path.join(basedir, "app", "static", "acts","default_act.docx")
    DEFAULT_WORD_DIR = os.path.join(basedir, "app", "static", "acts")
    PICS_DIR = os.path.join(basedir, "app", "static", "pics")