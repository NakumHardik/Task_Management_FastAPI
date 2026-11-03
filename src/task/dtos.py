from pydantic import BaseModel, ConfigDict


class TaskSchema(BaseModel):
    title: str
    description: str | None = None
    is_complated: bool = False


class TaskResponceSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None = None
    is_complated: bool
    user_id: int | None = None
