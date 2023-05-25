from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/tulip", tags=["tulip"], responses={404: {"message": "Sin usuarios registrados."}})
router.mount("/static", StaticFiles(directory="static"), name="static")
plantillas = Jinja2Templates(directory="plantillas")

@router.get("/catalogo", response_class=HTMLResponse)
async def catalogo(request: Request):
    return plantillas.TemplateResponse("catalogo_usuario.html", {"request": request})

@router.get("/contacto", response_class=HTMLResponse)
async def sucursales(request: Request):
    return plantillas.TemplateResponse("contacto_usuario.html", {"request": request})

@router.get("/inicio", response_class=HTMLResponse)
async def catalogo(request: Request):
    return plantillas.TemplateResponse("inicio_usuario.html", {"request": request})

@router.get("/nosotros", response_class=HTMLResponse)
async def catalogo(request: Request):
    return plantillas.TemplateResponse("nosotros_usuario.html", {"request": request})