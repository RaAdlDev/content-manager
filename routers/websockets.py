from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from ws.manager import manager
from models.user import User
from dependencies.auth import get_current_websocket
from database.connection import LocalSesion
from services.notifications_services import get_pending_notifications

router = APIRouter(prefix="/ws", tags=["WebSockets"])



@router.websocket("")
async def get_message( websocket: WebSocket, current_user :User = Depends(get_current_websocket)):

    with LocalSesion() as db:

        await manager.create_connection(websocket, current_user.user_id)

        notifications = get_pending_notifications(current_user.user_id, db)
        for n in notifications:
             
             await websocket.send_text(n.model_dump_json())
    try:
            while True:
                data = await websocket.receive_text()

    except WebSocketDisconnect:
            manager.remove_connection(current_user.user_id)

      

    
    
    
