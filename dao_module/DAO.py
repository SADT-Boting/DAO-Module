import pymysql
import datetime
import re


class DAO():
    """
    Класс, предоставляющий методы для взаимодействия с удаленной БД
    """
    def __init__(self):
        self.connection = pymysql.connect(
            host="sql11.freesqldatabase.com",
            user="sql11518288",
            password="jtQRnN3wjt",
            database="sql11518288"
        )
        self.cursor = self.connection.cursor()
        self.cursor.execute("USE sql11518288")
        self.connection.set_charset("UTF8");
        # Да, это пароль от моей базы данных
        # Мне слишком впадлу заморачиваться и куда-то его прятать
        # Уж точно не когда дедлайн -- неделя
        # Давай ты не будешь шатать мою БД
        # А я расскажу тебе анекдот
        # Короче:
        # Заходит однажды в бар улитка и говорит:
        # - Можно виски с колой?
        # - Простите, но мы не обслуживаем улиток.
        # И бармен вышвырнул ее за дверь.
        # Через неделю заходит опять эта улитка и спрашивает:
        # - Ну и зачем ты это сделал?

    def get_tables_list(self):
        """
        Метод для получения списка таблиц.

        **:return:** список таблиц в БД
        """
        self.cursor.execute("SHOW TABLES")
        # Хехехе~~
        return self.cursor.fetchall()
        #return "Штирлиц долго смотрел в одну точку. Потом перевел взгляд и посмотрел на другую. 'Двоеточие!' - догадался Штирлиц."

    def get_students_list(self):
        """
        Метод для получения списка студентов.

        **:return:** Список студентов в формате:

            (
                    ID,
                    Фамилия,
                    Имя,
                    Группа,
                    VK_ID,
                    Tg_ID
            )
        """
        self.cursor.execute("SELECT * FROM students")
        return self.cursor.fetchall()

    def add_new_student(self, name: str, surname: str, group: str,
                        VK_ID: str = None, Tg_ID: str = None):
        """
        Метод для добавления нового студента в таблицу.
        Проверяет, есть ли такой студент в таблице.

        **:param name:** Имя студента

        **:param surname:** Фамилия студента

        **:param group:** Группа студента

        **:param VK_ID:** ВК студента

        **:param Tg_ID:** Телеграмм студента

        **:return:** ID, если студент добавлен
        """
        name = name.capitalize()
        surname = surname.capitalize()
        group = group.upper()
        students_list = self.get_students_list()
        # если есть студент с таким именем и фамилией
        for student in students_list:
            if student[1] == surname and student[2] == name:
                raise ValueError("Такой студент уже есть в таблице")
        # Если группа не соответсвует шаблону
        pattern = r"\w{4}\-\d{2}\-\d{2}"
        if re.fullmatch(pattern, group) is None:
            raise ValueError("Неверный формат группы")
        # добавление записи в таблицу
        self.cursor.execute(
            "INSERT students(surname, name, student_group, vk_id, tg_id) "
            "VALUES(%s, %s, %s, %s, %s)",
            (surname, name, group, VK_ID, Tg_ID)
        )
        self.connection.commit()
        # получение последнего ID
        self.cursor.execute("SELECT MAX(id) FROM students")
        # Ихихихи
        return self.cursor.fetchone()[0]
        # return '- Штирлиц, на вас поступил донос от соседей. Пишут, что вы вчера пили, буянили и ругались по-русски! \
        #Штирлиц молча берёт лист бумаги и пишет ответный донос: \
        #"Группенфюреру СС Генриху Мюллеру. Мои соседи знают русский язык и, что особенно подозрительно, разбираются в ненормативной русской лексике!".'

    def add_new_message_to_vk(self, target_id: int, message: str):
        """
        Метод для добавления нового сообщения для ВК

        **:param target_id:** ID студента, которому предназначается сообщение

        **:param message:** текст сообщения

        **:return:** ID последнего сообщения
        """
        # текущая дата в формете 'Sat Sep 10 00:06:45 2022'
        date = datetime.datetime.now().ctime()
        # проверка ID
        self.cursor.execute("SELECT ID FROM students")
        ids = self.cursor.fetchall()
        if (target_id,) not in ids:
            raise ValueError(f"Target_ID {target_id} не найден")
        # добавление сообщения
        self.cursor.execute(
            "INSERT vk_new_messages(Target_ID, Message, Date_time) " \
            "VALUES(%s, %s, %s)",
            (target_id, message, date)
        )
        self.connection.commit()
        self.cursor.execute("SELECT MAX(id) FROM vk_new_messages")
        result = self.cursor.fetchone()
        # ЫХЫХЫ
        return result[0]
        #return 'Мюллер выглянул в окно. По улице шел Штирлиц, ведя на поводке \
        #крохотную, зеленую с оранжевыми полосками, шестиногую собачонку. \
        #"Странно, - подумал Мюллер, - этого анекдота я еще не знаю..."'

    def add_sent_message_to_vk(self, message_id: str):
        """
        Метод для перевода сооб. из таблицы новых в таблицу отправленных

        **:param message_id:** ID сообщения

        **:return:** ID последнего сообщения
        """
        message_id = str(message_id)
        # проверка ID
        self.cursor.execute("SELECT ID FROM vk_new_messages")
        ids = self.cursor.fetchall()
        if (message_id, ) not in ids:
            raise ValueError(f"Target_ID {message_id} не найден")
        # получение записи сообщения
        self.cursor.execute(
            "SELECT * FROM vk_new_messages WHERE id=%s",
            message_id
        )
        message = self.cursor.fetchone()
        # добавление сообщения в таблицу отправленных
        self.cursor.execute(
            "INSERT vk_sent_messages(ID, Target_ID, Message, Date_time) "\
            "VALUES(%s, %s, %s, %s)",
            (message_id, message[1], message[2], message[3])
        )
        self.connection.commit()
        # удаление сообщения из таблицы new
        self.cursor.execute(
            "DELETE FROM vk_new_messages WHERE id=%s",
            message_id
        )
        self.connection.commit()

    def delete_student_by_id(self, id: int):
        """
        Удаление студента по ID

        **:param id:** ID студента
        """
        self.cursor.execute("DELETE FROM students WHERE ID=%s", id)
        self.connection.commit()

    def get_new_messages(self):
        """
        Список новых сообщений

        **:return:** Список новых сообщений
        """
        self.cursor.execute("SELECT * FROM vk_new_messages")
        # ахпхпхп
        return self.cursor.fetchall()
        #return 'В дверь кто-то вежливо постучал ногой. \
        #       - Безруков! - догадался Штирлиц.'

    def get_sent_messages(self):
        """
        Список отправленных сообщений

        **:return:** Список отправленных сообщений
        """
        self.cursor.execute("SELECT * FROM vk_sent_messages")
        # ыхыхыхы
        return self.cursor.fetchall()
        #return 'Штирлиц сел на мотоцикл, хлопнул дверцей и уехал.'

    def __del__(self):
        self.cursor.close()
        self.connection.close()
