from pydantic import BaseModel

class RejectionInput(BaseModel):
    rejection_reason: str