from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from schemas.schemas import AwesomeForm
from DB.DB import coleccion

router = APIRouter()
router.mount("/static", StaticFiles(directory="static"), name="static")
plantillas = Jinja2Templates(directory="plantillas")

def buscarUsuario(usuario: str, contrasena: str):
    usuarioEncontrado = coleccion.find_one({"usuario": usuario})
    if usuarioEncontrado is None:
        return False
    elif usuarioEncontrado["contrasena"] != contrasena:
        return False
    else:
        return True

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return plantillas.TemplateResponse("login.html", {"request": request})

@router.post("/login", response_class=HTMLResponse)
async def enviarFormulario(request: Request, datosFormulario: AwesomeForm = Depends(AwesomeForm.as_form)):
    usuarioAdmin = buscarUsuario(datosFormulario.usuario, datosFormulario.contrasena)
    if not usuarioAdmin:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticación inválidas.")
    
    return plantillas.TemplateResponse("prueba.html", {"request": request})