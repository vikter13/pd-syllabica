# Конфигурация

SECRET_KEY = 'test_s_c'
DATABASE = '{instance}/users.sqlite'
QUIZESBASE = '{instance}/quiz/'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:acces_to_database@127.0.0.1:5432/syllabica'
SESSION_COOKIE_NAME = 'sylls'
# SERVER_NAME='.*'
LIVEDICT='NO'
BLUEPRINTS_TYPES='folders'