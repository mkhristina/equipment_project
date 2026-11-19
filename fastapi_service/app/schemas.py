
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class RequestCreate(BaseModel):
    equipment_id: int = Field(
        gt=0,
        description="ID оборудования должен быть положительным числом",
    )

    description: str = Field(
        min_length=1,
        description="Описание заявки",
    )

    priority: Literal["low", "medium", "high", "critical"] = "medium"

    @field_validator("description")
    @classmethod
    def description_not_blank(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError(
                "Описание заявки не может быть пустым."
            )

        return value
