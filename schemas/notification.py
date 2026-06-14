from pydantic import BaseModel, ConfigDict
from datetime import datetime

class NotificationInput(BaseModel):
    writer_user_id: str
    article_id: str
    message: str

class NotificationResponse(BaseModel):
    user_id: str
    article_id: str
    message: str
    is_read: bool
    notification_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)