from pydantic import BaseModel, ConfigDict

class TokenResponse(BaseModel):
    token: str
    token_type: str

    model_config = ConfigDict(from_attributes=True)