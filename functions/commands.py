from database import base
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


class Commands:
    def __init__(self):
        self.db = base.Database(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

    def group_exists(self, chat_id):
        response = self.db.fetch(f"SELECT COUNT(*) FROM groups WHERE chat_id = {chat_id}")[0][0]
        return bool(response)

    def add_group(self, msg):
        # print(msg.chat.id, msg.chat.title)
        self.db.execute(f"INSERT INTO groups (chat_id, name) VALUES ({msg.chat.id}, '{msg.chat.title}')")