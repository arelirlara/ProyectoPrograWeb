from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from esquemas.esquemas import DatosAutenticacion
from DB.DB import coleccion

router = APIRouter(prefix="/tulip", tags=["tulip"])
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
    
@router.get("/inicio", response_class=HTMLResponse)
async def inicio(request: Request):
    return plantillas.TemplateResponse("inicio_usuario.html", {"request": request})

@router.get("/catalogo", response_class=HTMLResponse)
async def catalogo(request: Request):
    return plantillas.TemplateResponse("catalogo_usuario.html", {"request": request})

@router.get("/contacto", response_class=HTMLResponse)
async def contacto(request: Request):
    return plantillas.TemplateResponse("contacto_usuario.html", {"request": request})

@router.get("/nosotros", response_class=HTMLResponse)
async def nosotros(request: Request):
    return plantillas.TemplateResponse("nosotros_usuario.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return plantillas.TemplateResponse("login.html", {"request": request})

@router.post("/login/success", response_class=HTMLResponse)
async def enviarFormulario(request: Request, datosFormulario: DatosAutenticacion = Depends(DatosAutenticacion.as_form)):
    usuarioAdmin = buscarUsuario(datosFormulario.usuario, datosFormulario.contrasena)
    if not usuarioAdmin:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticación inválidas.")
    
    return plantillas.TemplateResponse("catalogo_administrador.html", {"request": request})