import pymysql
import datetime
import re


class DAO():
    def __init__(self):
        """
        Конструктор. Устанавливает соединение с удаленной БД
        """
        self.connection = pymysql.connect(
            host="sql11.freesqldatabase.com",
            user="sql11518288",
            password="jtQRnN3wjt",
            database="sql11518288")
        self.cursor = self.connection.cursor()
        self.cursor.execute("USE sql11518288")

    def get_tables_list(self):
        """
        Метод для получения списка таблиц.
        :return: список таблиц в БД
        """
        dao.cursor.execute("SHOW TABLES")
        return dao.cursor.fetchall()

    def get_students_list(self):
        """
        Метод для получения списка студентов.
        :return: Список студентов в формате:
                ID,
                Фамилия,
                Имя,
                Группа,
                VK_ID,
                Tg_ID
        """
        dao.cursor.execute("SELECT * FROM students")
        return dao.cursor.fetchall()

    def add_new_student(self, name: str, surname: str, group: str, VK_ID: str = None, Tg_ID: str = None):
        """
        Метод для добавления нового студента в таблицу. Проверяет, есть ли такой студент в таблице.
        :param name: Имя студента
        :param surname: Фамилия студента
        :param group: Группа студента
        :param VK_ID: ВК студента
        :param Tg_ID: Телеграмм студента
        :return: True, если студент добавлен
                    False, если студент не добавлен
        """
        name = name.capitalize()
        surname = surname.capitalize()
        group = group.upper()
        students_list = self.get_students_list()
        # если есть студент с таким именем и фамилией
        for student in students_list:
            if student[1] == surname and student[2] == name:
                return False
        # Если группа не соответсвует шаблону
        pattern = r"\w{4}\-\d{2}\-\d{2}"
        if re.fullmatch(pattern, group) is None:
            return False
        # добавление записи в таблицу
        self.cursor.execute("INSERT Students(Surname, Name, Student_Group, VK_ID. Tg_ID) " \
                            "VALUES(%s, %s, %s, %s, %s)", surname, name, group, VK_ID, Tg_ID)
        return True

    def add_new_message_to_vk(self, target_ID: str, message: str):
        """
        Метод для добавления новой сообщения для ВК
        :param target_ID: ID студента, которому предназначается сообщение
        :param message: текст сообщения
        :return: ID последнего сообщения
        """
        date = datetime.datetime.now().ctime()
        # проверка ID
        self.cursor.execute("SELECT ID FROM Students")
        ids = self.cursor.fetchall()
        if target_ID not in ids:
            raise ValueError("Target_ID не найден")
        # добавление сообщения
        self.cursor.execute("INSERT vk_new_messages(Target_ID, Message, Data_time) " \
                            "VALUES(%s, %s, %s)", target_ID, message, date)
        self.cursor.execute("SELECT MAX(id) FROM vk_new_messages")
        return self.cursor.fetchone()

    def add_sent_message_to_vk(self, message_id: str):
        """
        Метод для перевода сообщения из таблицы новых в таблицу отправленных
        :param message_id: ID сообщения
        """
        message_id = str(message_id)
        # проверка ID
        self.cursor.execute("SELECT ID FROM vk_new_messages")
        ids = self.cursor.fetchall()
        if message_id not in ids:
            raise ValueError("Target_ID не найден")
        # получение записи сообщения
        self.cursor.execute("SELECT * FROM vk_new_messages WHERE id=%s", message_id)
        message = self.cursor.fetchone()
        # добавление сообщения в таблицу отправленных
        self.cursor.execute("INSERT vk_sent_messages(ID, Target_ID, Message, Data_time) "\
                            "VALUES(%s, %s, %s, %s)", message_id, message[1], message[2], message[3])
        # удаление сообщения из таблицы new
        self.cursor.execute("DELETE FROM vk_new_messages WHERE id=%s", message_id)

    def __del__(self):
        self.cursor.close()
        self.connection.close()


dao = DAO()
print(*dao.get_students_list(), sep='\n')
