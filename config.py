from dataclasses import dataclass


@dataclass
class MenuChoicer:
    START = """
1. Регистрация
2. Авторизация
3. Выход

Выберите действие: """

    CLIENT = """
1. Просмотр доступных занятий
2. Запись на занятие
3. Изменение своих данных
4. Выход

Выберите действие: """

    TRAINER = """
1. Просмотр клиентов, записанных к вам
2. Просмотр всех клиентов
3. Изменение своих данных
4. Выход

Выберите действие: """

    ADMIN = """
1. Просмотр и изменение типов карт
2. Просмотр и изменение типов занятий
3. Просмотр всех пользователей
4. Изменение своих данных
5. Выход

Выберите действие: """


DB_NAME = "fitnes_club.sqlite"


@dataclass
class RequestDB:
    class CreateTables:
        UsersTable = """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                full_name TEXT NOT NULL
            );
            """

        TypesCardsTable = """
            CREATE TABLE IF NOT EXISTS types_of_cards (
                card_id INTEGER PRIMARY KEY AUTOINCREMENT,
                card_type TEXT UNIQUE NOT NULL
            );
            """

        TypesActivitiesTable = """
            CREATE TABLE IF NOT EXISTS types_of_activities (
                activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
                activity_type TEXT UNIQUE NOT NULL
            );"""

        AppointmentsTable = """
            CREATE TABLE IF NOT EXISTS appointments (
                appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                activity_id INTEGER NOT NULL,
                trainer_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (activity_id) REFERENCES types_of_activities (activity_id),
                FOREIGN KEY (trainer_id) REFERENCES users (user_id)
            );"""

    class Add:
        InsertUserQuery = """
            INSERT INTO users (username, password, role, full_name) 
            VALUES (?, ?, ?, ?);
        """

        InsertTypeCardQuery = """
            INSERT INTO types_of_cards (card_type) VALUES (?);
        """

        AddTypeActivityQuery = """
            INSERT INTO types_of_activities (activity_type) VALUES (?);
        """

    class View:
        ViewTypesActivitiesQuery = """
            SELECT * FROM types_of_activities;
        """

        ViewAllTrainersQuery = """
            SELECT * FROM users WHERE role = "trainer";
        """

        ViewClientsTrainerQuery = """
            SELECT users.full_name, types_of_activities.activity_type
            FROM users
            JOIN appointments ON users.user_id = appointments.user_id
            JOIN types_of_activities ON appointments.activity_id = types_of_activities.activity_id
            WHERE appointments.trainer_id = ?;
        """

        ViewAllUsersQuery = """
            SELECT * FROM users;
        """

        ViewTypesCardsQuery = """
            SELECT * FROM types_of_cards;
        """

    class Get:
        GetUserQuery = """
            SELECT * FROM users WHERE username=? AND password=?;
        """

        GetUserDataQuery = """
            SELECT * FROM users WHERE user_id=?;
        """

    class Update:
        UpdateUserDataQuery = """
            UPDATE users SET full_name=? WHERE user_id=?;
        """

        UpdateTypeCardQuery = """
            UPDATE types_of_cards SET card_type=? WHERE card_id=?;
        """

        UpdateTypeActivityQuery = """
            UPDATE types_of_activities SET activity_type=? WHERE activity_id=?;
        """

        UpdateUserQuery = """
                UPDATE users 
                SET username=?, password=?, role=?, full_name=? 
                WHERE user_id=?;
        """

    class Delete:
        DeleteTypeActivityQuery = """
            DELETE FROM types_of_activities WHERE activity_id=?;
        """

        DeleteTypeCardQuery = """
            DELETE FROM types_of_cards WHERE card_id=?;
        """

        DeleteUserQuery = """
            DELETE FROM users WHERE user_id=?;
        """

    DataQuery = """
        INSERT OR IGNORE INTO types_of_cards (card_type) VALUES
            ("Basic"),
            ("Premium"),
            ("VIP");
        INSERT OR IGNORE INTO types_of_activities (activity_type) VALUES
            ("Yoga"),
            ("Pilates"),
            ("Cardio"),
            ("Weight Training");
    """

    MakeAppointmentQuery = """
        INSERT INTO appointments (user_id, activity_id, trainer_id)
        VALUES (?, ?, ?);
    """
