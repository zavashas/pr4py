import sqlite3

import config
import config as conf
from dataclasses import dataclass
from typing import Literal, Optional, Any
from abc import abstractmethod


@dataclass
class _User:
    idx: int
    login: str
    password: str
    role: Literal["client", "trainer", "admin"]
    full_name: str

    @abstractmethod
    def menu(self) -> None:
        pass

    def as_tuple(self) -> tuple[int, str, str, Literal['client', 'trainer', 'admin'], str]:
        return self.idx, self.login, self.password, self.role, self.full_name


class DataBase:
    __slots__ = ("__conn", "__cursor")

    def __init__(self, db_name: str) -> None:
        self.__conn = sqlite3.connect(db_name)
        self.__cursor = self.__conn.cursor()

    def init(self, init_data: bool = False) -> None:

        self.__cursor.execute(conf.RequestDB.CreateTables.AppointmentsTable)
        self.__conn.commit()

        self.__cursor.execute(conf.RequestDB.CreateTables.UsersTable)
        self.__cursor.execute(conf.RequestDB.CreateTables.TypesCardsTable)
        self.__cursor.execute(conf.RequestDB.CreateTables.TypesActivitiesTable)

        self.__conn.commit()

        if init_data is True:
            self.__cursor.executescript(conf.RequestDB.DataQuery)
            self.__conn.commit()

    def add_user(self, user: _User) -> None:

        self.__cursor.execute(conf.RequestDB.Add.InsertUserQuery, user.as_tuple()[1:])
        self.__conn.commit()

    def add_type_of_card(self, card_type: str) -> None:
        self.__cursor.execute(conf.RequestDB.Add.InsertTypeCardQuery, (card_type,))
        self.__conn.commit()

    def add_type_of_activity(self, activity_type: str) -> None:
        self.__cursor.execute(conf.RequestDB.Add.AddTypeActivityQuery, (activity_type,))
        self.__conn.commit()

    def get_user_by_credentials(self, username: str, password: str) -> Optional[_User]:
        try:
            self.__cursor.execute(conf.RequestDB.Get.GetUserQuery, (username, password))
            user_data = _User(*self.__cursor.fetchone())
            return user_data
        except TypeError:
            return None

    def get_user_data(self, user_id: int) -> Optional[_User]:
        self.__cursor.execute(conf.RequestDB.Get.GetUserDataQuery, (user_id,))
        data = self.__cursor.fetchone()
        if data is not None:
            user_data = _User(*data)
            return user_data
        else:
            print(f"Пользователь с ID {user_id} не найден.")
            return None

    def view_all_types_of_activities(self) -> None:
        self.__cursor.execute(conf.RequestDB.View.ViewTypesActivitiesQuery)
        types_of_activities = self.__cursor.fetchall()

        if types_of_activities:
            print("Список всех типов занятий:")
            for activity in types_of_activities:
                print(f"{activity[0]}. {activity[1]}")
            print()
        else:
            print("Типов занятий пока нет.\n")

    def view_all_users(self):
        self.__cursor.execute(conf.RequestDB.View.ViewAllUsersQuery)
        users = self.__cursor.fetchall()

        if users:
            print("Список всех пользователей:")
            for user in users:
                user = _User(*user)
                print(f"{user.idx}. {user.login} - {user.full_name} ({user.role})")
            print()
        else:
            print("Пользователей пока нет.\n")

    def update_user_data(self, user_id: int, new_full_name: str) -> None:
        self.__cursor.execute(conf.RequestDB.Update.UpdateUserDataQuery, (new_full_name, user_id))
        self.__conn.commit()

    def update_type_of_card(self, card_id: int, new_card_type: str) -> None:
        self.__cursor.execute(conf.RequestDB.Update.UpdateTypeCardQuery, (new_card_type, card_id))
        self.__conn.commit()

    def update_type_of_activity(self, activity_id: int, new_activity_type: str) -> None:
        self.__cursor.execute(conf.RequestDB.Update.UpdateTypeActivityQuery, (new_activity_type, activity_id))
        self.__conn.commit()

    def update_user(self, user_id: int, new_username: str, new_password: str, new_role: str,
                    new_full_name: str) -> None:
        self.__cursor.execute(conf.RequestDB.Update.UpdateUserQuery,
                              (new_username, new_password, new_role, new_full_name, user_id))
        self.__conn.commit()

    def delete_type_of_activity(self, activity_id: int) -> None:
        self.__cursor.execute(conf.RequestDB.Delete.DeleteTypeActivityQuery, (activity_id,))
        self.__conn.commit()

    def delete_type_of_card(self, card_id: int) -> None:
        self.__cursor.execute(conf.RequestDB.Delete.DeleteTypeCardQuery, (card_id,))
        self.__conn.commit()

    def delete_user(self, user_id: int) -> None:
        self.__cursor.execute(conf.RequestDB.Delete.DeleteUserQuery, (user_id,))
        self.__conn.commit()

    def make_appointment(self, user_id: int, activity_id: int, trainer_id: int) -> None:
        trainer_id = trainer_id if trainer_id is not None else 'NULL'

        self.__cursor.execute(config.RequestDB.MakeAppointmentQuery, (user_id, activity_id, trainer_id))
        self.__conn.commit()

    def close_connection(self) -> None:

        self.__conn.close()

    def exec(self, query: str, *args) -> None:
        self.__cursor.execute(query, args)

    def fetch(self) -> list[Any, ...]:
        return self.__cursor.fetchall()
