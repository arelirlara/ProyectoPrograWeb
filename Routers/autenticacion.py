from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from schemas.schemas import AwesomeForm

router = APIRouter()
router.mount("/static", StaticFiles(directory="static"), name="static")
plantillas = Jinja2Templates(directory="plantillas")

def buscarUsuario(usuario: str, contrasena: str):
    for i in range(len(usuariosAdmin)):
        if usuariosAdmin[i]["usuario"] == usuario and usuariosAdmin[i]["contrasena"] == contrasena:
            return True

usuariosAdmin = [{
    "usuario": "OscarDev2345",
    "contrasena": "123456"
},
{
    "usuario": "AreliDev9087",
    "contrasena": "098765"
}]

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return plantillas.TemplateResponse("login.html", {"request": request})

@router.post("/login", response_class=HTMLResponse)
async def enviarFormulario(request: Request, datosFormulario: AwesomeForm = Depends(AwesomeForm.as_form)):
    usuarioAdmin = buscarUsuario(datosFormulario.usuario, datosFormulario.contrasena)
    if not usuarioAdmin:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticación inválidas.")
    
    return plantillas.TemplateResponse("prueba.html", {"request": request})