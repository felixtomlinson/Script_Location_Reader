import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'lolthisismysecretkey'
    UPLOAD_FOLDER = '/scripts'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False