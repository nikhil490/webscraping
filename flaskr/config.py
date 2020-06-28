import os
from scrapyspider.spiders.springer_doi import SpringerDoi
from scrapyspider.spiders.wiley_doi import WileyDoi
from scrapyspider.spiders.ieee_doi import IeeeDoi
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'dev'
    ALLOWED_EXTENSIONS = {'csv', 'json'}
    DICT_OF_SPIDERS = {'springer': SpringerDoi, 'wiley': WileyDoi, 'ieee': IeeeDoi}
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')


