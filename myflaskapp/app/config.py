# Секретный ключ для Flask
SECRET_KEY = 'b7e50f64b446eb34c2fd48b1b84af65d'

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@localhost/db'
# SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password@192.168.1.2/db'

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True