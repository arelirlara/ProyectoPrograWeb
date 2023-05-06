from fastapi import Form
from pydantic import BaseModel

class AwesomeForm(BaseModel):
    usuario: str
    contrasena: str

    @classmethod
    def as_form(
        cls,
        usuario: str = Form(...),
        contrasena: str = Form(...),
    ):
        return cls(
            usuario=usuario,
            contrasena=contrasena,
        )