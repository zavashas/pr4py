from base import _User, DataBase
import config as conf


class Client(_User):
    db: DataBase

    def connect_to_db(self, db: DataBase):
        self.db = db

    def menu(self) -> None:
        self.__loop()

    def __loop(self) -> None:
        while True:
            client_choice = input(conf.MenuChoicer.CLIENT).strip()

            if client_choice == "1":
                self.db.view_all_types_of_activities()
            elif client_choice == "2":
                self.db.view_all_types_of_activities()
                try:
                    activity_id = int(input("Введите ID занятия для записи: "))
                except ValueError:
                    print("Неверный ввод. Введите целое число.")
                    continue

                self.view_all_trainers()
                try:
                    trainer_id = int(input("Введите ID тренера (оставьте пустым, если не выбран): ") or 0)
                except ValueError:
                    print("Неверный ввод. Введите целое число.")
                    continue

                self.db.make_appointment(self.idx, activity_id, trainer_id)
                print("Вы успешно записаны на занятие!\n")
            elif client_choice == "3":
                new_full_name = input("Введите новое полное имя: ")
                self.db.update_user_data(self.idx, new_full_name)
                print("Данные пользователя успешно изменены!\n")
            elif client_choice == "4":
                print("Выход из аккаунта.\n")
                break
            else:
                print("Неверный выбор. Повторите попытку.\n")

    def view_all_trainers(self) -> None:
        self.db.exec(conf.RequestDB.View.ViewAllTrainersQuery)
        trainers = self.db.fetch()

        if trainers:
            print("Список всех тренеров:")
            for trainer in trainers:
                print(f"{trainer[0]}. {trainer[4]}")
            print()
        else:
            print("Тренеров пока нет.\n")


class Trainer(_User):
    db: DataBase

    def connect_to_db(self, db: DataBase):
        self.db = db

    def menu(self) -> None:
        self.__loop()

    def __loop(self) -> None:
        while True:
            trainer_choice = input(conf.MenuChoicer.TRAINER)

            if trainer_choice == "1":
                self.view_clients_for_trainer()
            elif trainer_choice == "2":
                self.db.view_all_users()
            elif trainer_choice == "3":
                new_full_name = input("Введите новое полное имя: ")
                self.db.update_user_data(self.idx, new_full_name)
                print("Данные пользователя успешно изменены!\n")
            elif trainer_choice == "4":
                print("Выход из аккаунта.\n")
                break
            else:
                print("Неверный выбор. Повторите попытку.\n")

    def view_clients_for_trainer(self) -> None:
        self.db.exec(conf.RequestDB.View.ViewClientsTrainerQuery, self.idx)
        clients = self.db.fetch()

        if clients:
            print("Список клиентов, записанных к вам:")
            for client in clients:
                print(f"{client[0]} - {client[1]}")
            print()
        else:
            print("У вас нет записанных клиентов.\n")


class Admin(_User):
    db: DataBase

    def connect_to_db(self, db: DataBase):
        self.db = db

    def menu(self) -> None:
        self.__loop()

    def __loop(self) -> None:
        while True:
            admin_choice = input(conf.MenuChoicer.ADMIN)

            if admin_choice == "1":
                self.change_card()
            elif admin_choice == "2":
                self.change_activity()
            elif admin_choice == "3":
                self.config_users()
            elif admin_choice == "4":
                new_full_name = input("Введите новое полное имя: ")
                self.db.update_user_data(self.idx, new_full_name)
                print("Данные пользователя успешно изменены!\n")
            elif admin_choice == "5":
                print("Выход из аккаунта.\n")
                break
            else:
                print("Неверный выбор. Повторите попытку.\n")

    def change_card(self) -> None:
        self.view_all_types_of_cards()
        admin_action = input("Выберите действие (1 - добавить, 2 - изменить, 3 - удалить, 4 - назад): ")
        if admin_action == "1":
            new_card_type = input("Введите новый тип карты: ")
            self.db.add_type_of_card(new_card_type)
            print("Тип карты успешно добавлен!\n")
        elif admin_action == "2":
            try:
                card_id = int(input("Введите ID типа карты для изменения: "))
            except ValueError:
                print("Неверный ввод. Введите целое число.")
                return

            new_card_type = input("Введите новый тип карты: ")
            self.db.update_type_of_card(card_id, new_card_type)
            print("Тип карты успешно изменен!\n")
        elif admin_action == "3":
            try:
                card_id = int(input("Введите ID типа карты для удаления: "))
            except ValueError:
                print("Неверный ввод. Введите целое число.")
                return

            self.db.delete_type_of_card(card_id)
            print("Тип карты успешно удален!\n")
        elif admin_action == "4":
            pass

    def change_activity(self) -> None:
        self.db.view_all_types_of_activities()
        admin_action = input("Выберите действие (1 - добавить, 2 - изменить, 3 - удалить, 4 - назад): ")
        if admin_action == "1":
            new_activity_type = input("Введите новый тип занятия: ")
            self.db.add_type_of_activity(new_activity_type)
            print("Тип занятия успешно добавлен!\n")
        elif admin_action == "2":
            try:
                activity_id = int(input("Введите ID типа занятия для изменения: "))
            except ValueError:
                print("Неверный ввод. Введите целое число.")
                return

            new_activity_type = input("Введите новый тип занятия: ")
            self.db.update_type_of_activity(activity_id, new_activity_type)
            print("Тип занятия успешно изменен!\n")
        elif admin_action == "3":
            try:
                activity_id = int(input("Введите ID типа занятия для удаления: "))
            except ValueError:
                print("Неверный ввод. Введите целое число.")
                return

            self.db.delete_type_of_activity(activity_id)
            print("Тип занятия успешно удален!\n")
        elif admin_action == "4":
            pass

    def config_users(self) -> None:
        self.db.view_all_users()
        admin_action = input("Выберите действие (1 - добавить, 2 - изменить, 3 - удалить, 4 - назад): ")
        if admin_action == "1":
            self.__add_user()
        elif admin_action == "2":
            try:
                user_id = int(input("Введите ID пользователя для изменения: "))
            except ValueError:
                print("Неверный ввод. Введите целое число.")
                return

            current_user_data = self.db.get_user_data(user_id)

            if current_user_data:
                print("Текущие данные пользователя:")
                print(f"Логин: {current_user_data.login}")
                print(f"Пароль: {current_user_data.password}")
                print(f"Роль: {current_user_data.role}")
                print(f"Полное имя: {current_user_data.full_name}")

                new_username = input("Введите новый логин (оставьте пустым, чтобы не изменять): ")
                new_password = input("Введите новый пароль (оставьте пустым, чтобы не изменять): ")
                new_role = input("Введите новую роль (оставьте пустым, чтобы не изменять): ")
                new_full_name = input("Введите новое полное имя (оставьте пустым, чтобы не изменять): ")

                new_username = new_username if new_username else current_user_data.login
                new_password = new_password if new_password else current_user_data.password
                new_role = new_role if new_role else current_user_data.role
                new_full_name = new_full_name if new_full_name else current_user_data.full_name

                self.db.update_user(user_id, new_username, new_password, new_role, new_full_name)
                print("Данные пользователя успешно изменены!\n")
            else:
                print("Пользователь с указанным ID не найден.\n")
        elif admin_action == "3":
            try:
                user_id = int(input("Введите ID пользователя для удаления: "))
            except ValueError:
                print("Неверный ввод. Введите целое число.")
                return

            self.db.delete_user(user_id)
            print("Пользователь успешно удален!\n")
        elif admin_action == "4":
            pass
        else:
            print("Неверный выбор. Повторите попытку.\n")

    def __add_user(self) -> None:
        new_username = input("Введите логин нового пользователя: ")
        new_password = input("Введите пароль нового пользователя: ")
        new_role = input("Выберите роль нового пользователя (client/trainer/admin): ")
        new_full_name = input("Введите полное имя нового пользователя: ")

        user_data = _User(0, new_username, new_password, new_role, new_full_name)
        self.db.add_user(user_data)
        print("Пользователь успешно добавлен!\n")

    def view_all_types_of_cards(self) -> None:
        self.db.exec(conf.RequestDB.View.ViewTypesCardsQuery)
        types_of_cards = self.db.fetch()

        if types_of_cards:
            print("Список всех типов карт:")
            for card in types_of_cards:
                print(f"{card[0]}. {card[1]}")
            print()
        else:
            print("Типов карт пока нет.\n")
