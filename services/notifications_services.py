from models.notification import Notification
from sqlalchemy.orm import Session
from sqlalchemy import select
from schemas.notification import NotificationInput, NotificationResponse
from ws.manager import manager
from database.connection import LocalSesion

async def new_notification(notification_data: NotificationInput ):
    with LocalSesion() as db:
        notification = Notification(
        user_id = notification_data.writer_user_id,
        article_id = notification_data.article_id,
        message = notification_data.message
        )



        if notification_data.writer_user_id in manager.active_connections:
            notification.is_read = True
        db.add(notification)
        db.commit()
        db.refresh(notification)
        response_data = NotificationResponse.model_validate(notification)


    await manager.send_message(notification_data.writer_user_id, response_data.model_dump_json())
    


def get_pending_notifications(user_id: str, db: Session):
    notifications = db.execute(select(Notification).where(Notification.user_id == user_id, Notification.is_read == False)).scalars().all()
    response = [NotificationResponse.model_validate(n) for n in notifications ]
    for n in notifications:
        n.is_read = True
    db.commit()
    return response


