import sqlite3


class DB:
    def __init__(self, name):
        self.__db = name
        self.__connection = sqlite3.connect(self.__db)
        self.__connection.row_factory = sqlite3.Row  # записи в виде словаря
        self.__cursor = self.__connection.cursor()

    def close_connection(self):
        self.__cursor.close()
        self.__connection.close()
        print('BD connection was closed')

    def get_user_password(self, username):
        sql = "select password from users where username=='{username}'".format(username=username)
        try:
            result = self.__cursor.execute(sql).fetchone()
            self.close_connection()
            return result
        except Exception as e:
            print(f'Error: {e}')
        return None

    def get_user_info(self, username):
        sql = "select * from users where username=='{username}'".format(username=username)
        try:
            result = self.__cursor.execute(sql).fetchone()
            self.close_connection()
            return result
        except Exception as e:
            print(f'Error: {e}')
        return None

    def get_user_info_by_id(self, user_id):
        sql = "select * from users where id=='{userid}'".format(userid=user_id)
        try:
            result = self.__cursor.execute(sql).fetchone()
            self.close_connection()
            return result
        except Exception as e:
            print(f'Error: {e}')
        return None

    def add_user(self, data):
        sql = "insert into users (username, password) values ('{username}', '{password}')".format(
            username=data['username'], password=data['password'])
        try:
            self.__cursor.execute(sql)
            self.__connection.commit()
            self.close_connection()
            return True
        except Exception as e:
            print(f'Error: {e}')
        return False

    def add_post(self, data) -> bool:
        sql = "insert into posts (title, full_text, author) values ('{title}', '{text}', '{author}')".format(title=data['title'], text=data['text'], author=data['author'])
        try:
            self.__cursor.execute(sql)
            self.__connection.commit()
            self.close_connection()
            return True
        except Exception as e:
            print(f'Error: {e}')
        return False

    def get_posts(self):
        sql = "select * from posts"
        try:
            result = self.__cursor.execute(sql).fetchall()
            self.close_connection()
            return result
        except Exception as e:
            print(f'Error: {e}')
        return None

    def get_post(self, post_id):
        sql = "select * from posts where id={id}".format(id=post_id)
        try:
            result = self.__cursor.execute(sql).fetchone()
            self.close_connection()
            return result
        except Exception as e:
            print(f'Error: {e}')
        return None

    def updateUserAvatar(self, avatar, user_id):
        if not avatar:
            return False

        try:
            binary = sqlite3.Binary(avatar)
            self.__cursor.execute(f"UPDATE users SET avatar = ? WHERE id = ?", (binary, user_id))
            self.__connection.commit()
        except sqlite3.Error as e:
            print("Ошибка обновления аватара в БД: " + str(e))
            return False
        return True
