class DB:
    def __init__(self, db):
        self.__db = db
        self.__cursor = db.cursor()

    def get_user(self, username):
        sql = "select password from users where username=='{username}'".format(username=username)
        try:
            result = self.__cursor.execute(sql).fetchone()
            return result
        except Exception as e:
            print(f'Error: {e}')
        return None

    def add_user(self, data):
        sql = "insert into users (username, password) values ('{username}', '{password}')".format(
            username=data['username'], password=data['password'])
        try:
            result = self.__cursor.execute(sql)
            self.__db.commit()
            return True
        except Exception as e:
            print(f'Error: {e}')
        return False

    def add_post(self, data) -> bool:
        sql = "insert into posts (title, full_text, author) values ('{title}', '{text}', '{author}')".format(title=data['title'], text=data['text'], author=data['author'])
        try:
            result = self.__cursor.execute(sql)
            self.__db.commit()
            return True
        except Exception as e:
            print(f'Error: {e}')
        return False

    def get_posts(self):
        sql = "select * from posts"
        try:
            result = self.__cursor.execute(sql).fetchall()
            return result
        except Exception as e:
            print(f'Error: {e}')
        return None

    def get_post(self, post_id):
        sql = "select * from posts where id={id}".format(id=post_id)
        try:
            result = self.__cursor.execute(sql).fetchone()
            return result
        except Exception as e:
            print(f'Error: {e}')
        return None
