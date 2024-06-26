import datetime

class ChatMessage:
    def __init__(self, id: int, chat_box_id: int, message: str, sender: str, timestamp: datetime.datetime):
        self.id = id
        self.chat_box_id = chat_box_id
        self.message = message
        self.sender = sender
        self.timestamp = timestamp

class ChatBox:
    def __init__(self, id: int, user_id: int, name: str, created_at: datetime.datetime):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.created_at = created_at