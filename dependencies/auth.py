from database.connection import get_db, LocalSesion
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from core.settings import settings
from core.security import oauth
from jose import jwt, JWTError
from models.user import User
from fastapi import Query, WebSocket, WebSocketException

def get_current_user(db: Session = Depends(get_db),  token = Depends(oauth)):
    try:
        data = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id = data.get("sub")
        user = db.get(User, user_id)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        if not user.is_active:
            raise HTTPException(status_code=403, detail="Inactive user")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Not Allowed")
    
async def get_current_websocket(websocket: WebSocket, token: str = Query(None)):
    if not token:
        await websocket.accept()
        await websocket.close(code=1008)
        raise WebSocketException(code=1008, reason="Token Missing")
    try:
        data = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id = data.get("sub")
        db = LocalSesion()
        user = db.get(User, user_id)
        db.close()
        if not user:
            await websocket.close(code=1008)
            raise WebSocketException(code=1008, reason="Invalid Credentials")
        if not user.is_active:
            await websocket.close()
            raise WebSocketException(code=1008, reason="Inactive User")
        return user
    except JWTError:
        websocket.close(code=1800)
        raise WebSocketException(code=1008, reason="Not Allowed")
    