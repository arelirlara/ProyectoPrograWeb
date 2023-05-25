from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from DB.DB import coleccionSucursales
from esquemas.esquemas import DatosSucursales, sucursalesEsquema
from bson import ObjectId

router = APIRouter(prefix="/sucursales", tags=["sucursales"], responses={404: {"message": "Sin sucursales registrados."}})
router.mount("/static", StaticFiles(directory="static"), name="static")
plantillas = Jinja2Templates(directory="plantillas")

@router.get("/", response_model=list[DatosSucursales])
async def listaSucursales():
    return sucursalesEsquema(coleccionSucursales.find())

@router.get("/nueva_sucursal", response_class=HTMLResponse)
async def nuevaSucursal(request: Request):
    return plantillas.TemplateResponse("p13.html", {"request": request})

@router.post("/nueva_sucursal", response_class=HTMLResponse)
async def nuevaSucursal(request: Request, sucursal: DatosSucursales):
    # Obtener los datos del formulario enviado en la solicitud POST
    form_data = await request.form()

    nombre_sucursal = form_data.get('inputNombre')
    telefono_sucursal = form_data.get('inputTelefono')
    celular_sucursal = form_data.get('inputCelular')
    direccion_sucursal = form_data.get('inputDireccion')
    url = form_data.get('inputURL')

    sucursal = sucursal(nombreSucursal=nombre_sucursal, telefonoSucursal=telefono_sucursal, celularSucursal=celular_sucursal, direccionSucursal=direccion_sucursal, url=url)

    coleccionSucursales.insert_one(sucursal.dict())

@router.post("/crear_sucursal")
async def crearSucursal(request: Request):
    form_data = await request.form()
    
    nombre_sucursal = form_data.get('inputNombre')
    telefono_sucursal = form_data.get('inputTelefono')
    celular_sucursal = form_data.get('inputCelular')
    direccion_sucursal = form_data.get('inputDireccion')
    url = form_data.get('inputURL')
    
    sucursal = {
        "nombre": nombre_sucursal,
        "telefono": telefono_sucursal,
        "celular": celular_sucursal,
        "direccion": direccion_sucursal,
        "urlMaps": url
    }

    coleccionSucursales.insert_one(sucursal)

    return {"message": "Sucursal agregada correctamente"}

@router.put("/editar_sucursal", response_model=DatosSucursales)
async def user(sucursal: DatosSucursales):
        sucursal_diccionario = dict(sucursal)
        del sucursal_diccionario["id"]

        try:
            coleccionSucursales.find_one_and_replace({"_id": ObjectId(sucursal.id)}, sucursal_diccionario)
        except:
            return {"error": "No se ha actualizado el producto."}
        
        return buscarSucursal("_id", ObjectId(sucursal.id))

@router.delete("/eliminar_sucursal/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminarSucursal(id: str):
    encontrado = coleccionSucursales.find_one_and_delete({"_id": ObjectId(id)})

    if not encontrado:
        return {"error": "No se ha encontrado la sucursal."}

def buscarSucursal(field: str, key):
    try:
        sucursal = coleccionSucursales.find_one({field: key})
        return DatosSucursales(sucursalesEsquema(sucursal))
    except:
        return {"error": "No se ha encontrado sucursal."}