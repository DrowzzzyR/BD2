# from flask_login import current_user

# Политики доступа к ресурсам
# Класс имеет в себе набор методов, каждый из которых отвечает за определенные действия
class UsersPolicy:
    def __init__(self, record):
		# Передаем запись из БД, над которой будут производиться действия
        self.record = record

    # def is_admin(self):
    #     return current_user.is_admin()