import datetime

from sqlmodel import Field, SQLModel


class Birthday(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    name: str = Field(index=True)
    date: datetime.date
