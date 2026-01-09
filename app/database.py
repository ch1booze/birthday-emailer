import csv
from datetime import datetime
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine, select

from .environment import DATABASE_URI
from .models import Birthday

connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URI, connect_args=connect_args)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_db():
    with Session(engine) as session:
        yield session


def seed_db():
    with Session(engine) as session:
        with open("data/birthdays.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                existing_birthday = session.exec(
                    select(Birthday).where(Birthday.email == row["email"])
                ).first()

                if not existing_birthday:
                    new_birthday = Birthday(
                        name=row["name"],
                        email=row["email"],
                        date=datetime.strptime(
                            f"{row['birth_year']}-{row['birth_month']}-{row['birth_day']}",
                            "%Y-%m-%d",
                        ).date(),
                    )
                    session.add(new_birthday)

            session.commit()


SessionDep = Annotated[Session, Depends(get_db)]
