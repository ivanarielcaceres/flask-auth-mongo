class Config(object):
    DEBUG = False
    SECRET_KEY = 'sdafdkjhsfmcvbbasjjsafghghgsd\sa'
    MONGODB_SETTINGS = {'db': 'myrestfulapi2'}

class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


# class MongoDB(DB):
#     """URL FORMAT - mongodb://username:password@host:port/database?options"""
#     db = ''
#     host = ''
#     port = 27100
#     username = ''
#     password = ''
#     url = "mongodb://{}:{}@{}:{}/{}".format(
#         username, password, host, port, db)