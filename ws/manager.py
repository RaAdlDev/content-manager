from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def create_connection(self, websocket: WebSocket, user_id: str):
        await websocket.accept()

        self.active_connections[user_id] = websocket
    def remove_connection(self, user_id:str):

        self.active_connections.pop(user_id, None)
    async def send_message(self, user_id: str, message: dict):
        if user_id not in self.active_connections:
            return
        await self.active_connections[user_id].send_text(message)

manager = ConnectionManager()
