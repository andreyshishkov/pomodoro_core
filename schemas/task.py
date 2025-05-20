from pydantic import BaseModel, Field, model_validator


class TaskSchema(BaseModel):
    id: int | None
    name: str | None = None
    pomodoro_number: int | None = None
    category_id: int = Field(exclude=True)

    class Config:
        from_attributes = True

    @model_validator(mode='after')
    def check_name_or_pomodoro_num_is_not_none(self):
        if self.name is None and self.pomodoro_number is None:
            raise ValueError('name or pomodoro_number must be provided')
        return self
