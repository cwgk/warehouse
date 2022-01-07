import os
from warehouse import app

# DEBUG = True
# DIALECT = 'mysql'
# DRIVER = "pymysql"
# USERNAME = 'root'
# PASSWORD = '8269961'
# HOST = '127.0.0.1'
# PORT = '3306'
# DATABASE = 'mywh'
# SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
#     DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
# )
# SQLALCHEMY_COMMIT_ON_TEARDOWN = True
# SQLALCHEMY_TRACK_MODIFICATIONS = True
# SQLALCHEMY_POOL_SIZE = 10
# SQLALCHEMY_MAX_OVERFLOW = 5

dev_db = 'sqlite:///' + os.path.join(os.path.dirname(app.root_path), 'data.db')
SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', dev_db)
DEBUG_TB_INTERCEPT_REDIRECTS = False
SAYHELLO_POST_PER_PAGE = 20
