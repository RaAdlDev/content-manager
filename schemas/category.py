from pydantic import BaseModel, ConfigDict


class CategoryInput(BaseModel):
    name:str

class CategoryOutput(BaseModel):
    name: str
    slug: str
    
    model_config = ConfigDict(from_attributes=True)
