from pydantic import BaseModel, ConfigDict


class TagInput(BaseModel):
    name: str


class TagOutput(BaseModel):
    name: str
    slug: str

    model_config = ConfigDict(from_attributes=True)