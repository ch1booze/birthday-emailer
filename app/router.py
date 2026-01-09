import datetime
from typing import Annotated

from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel, select

from .database import SessionDep
from .models import Birthday

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


class AddBirthdayForm(SQLModel):
    name: str
    email: str
    birthday: datetime.date

class EditBirthdayForm(AddBirthdayForm):
    id: str


@router.get("/")
def index(request: Request, session: SessionDep):
    found_birthdays = session.exec(select(Birthday).order_by(Birthday.date)).all()
    return templates.TemplateResponse(
        name="index.html", request=request, context={"data": found_birthdays}
    )


@router.get("/add")
def add_form(request: Request):
    return templates.TemplateResponse(name="add.html", request=request)


@router.post("/add")
def add(
    request: Request, form: Annotated[AddBirthdayForm, Form()], session: SessionDep
):
    new_birthday = Birthday(name=form.name, email=form.email, date=form.birthday)
    session.add(new_birthday)
    session.commit()

    return RedirectResponse(url="/", status_code=303)


@router.get("/edit")
def edit_form(request: Request, email: str, session: SessionDep):
    found_birthday = session.exec(
        select(Birthday).where(Birthday.email == email)
    ).first()
    if found_birthday:
        return templates.TemplateResponse(
            name="edit.html",
            request=request,
            context={
                "name": found_birthday.name,
                "email": found_birthday.email,
                "birthday": found_birthday.date,
            },
        )

    return RedirectResponse(url="/", status_code=303)


@router.post("/edit")
def edit(form: Annotated[EditBirthdayForm, Form()], session: SessionDep):
    birthday_to_update = session.exec(
        select(Birthday).where(Birthday.email == form.id)
    ).first()
    if birthday_to_update:
        birthday_to_update.email = form.email
        birthday_to_update.name = form.name
        birthday_to_update.date = form.birthday
        session.add(birthday_to_update)
        session.commit()
        session.refresh(birthday_to_update)

    return RedirectResponse(url="/", status_code=303)


@router.get("/delete")
def delete(request: Request, email: str, session: SessionDep):
    birthday_to_delete = session.exec(
        select(Birthday).where(Birthday.email == email)
    ).first()
    if birthday_to_delete:
        session.delete(birthday_to_delete)
        session.commit()

    return RedirectResponse(url="/", status_code=303)
