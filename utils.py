import sqlite3

from base import DataBase, _User
from typing import Optional, assert_never
from warnings import warn
from users import Client, Admin, Trainer


class DatabaseManager:
    name: str
    __db: DataBase

    def __init__(self, db_name: str) -> None:
        self.name = db_name

    def __enter__(self) -> Optional[DataBase]:
        try:
            self.__db = DataBase(self.name)
        except sqlite3.Error as exc:
            warn(f"Ошибка подключения к базе данных: {exc}")
        else:
            return self.__db

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        try:
            self.__db.close_connection()
        except AttributeError:
            warn("Отключение базы данных не реализованно")
        except sqlite3.Error as exc:
            warn(f"Во время закрытия базы данных произошла ошибка: {exc}")


def register_user_in_db(db: DataBase) -> None:
    while True:
        login = input("Регистрация нового пользователя\nВведите логин: ").strip()
        password = input("Введите пароль: ").strip()
        full_name = input("Введите ФИО: ").strip()

        if not all([login, password, full_name]):
            print("Все поля должны быть заполнены. Повторите ввод.")
        else:
            break

    while True:
        role = input("Выберите роль (клиент [с] / тренер [т] / админ [а]): ").strip().lower()
        if role not in ('с', 'т', 'а'):
            print("Неверный формат ввода!")
            continue

        match role:
            case 'с':
                role = 'client'
            case 'т':
                role = 'trainer'
            case 'а':
                role = 'admin'
        break

    user_data = _User(idx=0, login=login, password=password, full_name=full_name, role=role)
    db.add_user(user=user_data)

    print("Пользователь успешно зарегистрирован")



def login_in_db(db: DataBase) -> Optional[Admin | Client | Trainer]:

    username = input("Авторизация\nВведите логин: ")
    password = input("Введите пароль: ")

    user_data = db.get_user_by_credentials(username, password)

    if user_data is not None:
        print(f"Добро пожаловать, {user_data.full_name} ({user_data.role})!\n")

        match user_data.role:
            case "client":
                user = Client(*user_data.as_tuple())
            case "trainer":
                user = Trainer(*user_data.as_tuple())
            case "admin":
                user = Admin(*user_data.as_tuple())
            case _ as unreachable:
                assert_never(unreachable)

        return user
    else:
        print("Неправильный логин или пароль. Повторите попытку.\n")
        return None
