import config as conf
from utils import DatabaseManager, register_user_in_db, login_in_db
from config import DB_NAME
from base import _User, DataBase
from users import Client, Trainer, Admin


def get_user(db: DataBase) -> _User:
    while True:
        choice = input(conf.MenuChoicer.START).strip()

        match choice:
            case "1":
                register_user_in_db(db)
            case "2":
                user_data = login_in_db(db)
                if user_data is None:
                    continue
                return user_data
            case "3":
                break
            case _:
                print("Неверный выбор. Повторите попытку.\n")


def main():
    with DatabaseManager(DB_NAME) as db:
        if db is not None:
            db.init(init_data=True)

            user_data = get_user(db)

            match user_data.role:
                case "client":
                    user = Client(*user_data.as_tuple())
                case "trainer":
                    user = Trainer(*user_data.as_tuple())
                case "admin":
                    user = Admin(*user_data.as_tuple())

            user.connect_to_db(db)
            user.menu()


if __name__ == '__main__':
    main()
