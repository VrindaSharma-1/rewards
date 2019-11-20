import os

SECRET_KEY = 'fd567d26fd9e577e3acc45ebff9a0994'

PROJECT_ID = 'rewardssys'

CLOUDSQL_USER = 'root'
CLOUDSQL_PASSWORD = 'password'
CLOUDSQL_DATABASE = 'rewards'
CLOUDSQL_CONNECTION_NAME = 'rewardssys:us-central1:rewards'
LOCAL_SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{user}:{password}@127.0.0.1:3306/{database}').format(
        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
        database=CLOUDSQL_DATABASE)
LIVE_SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{user}:{password}@localhost/{database}'
    '?unix_socket=/cloudsql/{connection_name}').format(
    user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
    database=CLOUDSQL_DATABASE, connection_name=CLOUDSQL_CONNECTION_NAME)

if os.environ.get('GAE_INSTANCE'):
    SQLALCHEMY_DATABASE_URI = LIVE_SQLALCHEMY_DATABASE_URI
else:
    SQLALCHEMY_DATABASE_URI = LOCAL_SQLALCHEMY_DATABASE_URI
