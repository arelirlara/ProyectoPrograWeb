from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from DB.DB import coleccionProductos
from esquemas.esquemas import DatosProducto, productosEsquema
from bson import ObjectId

router = APIRouter(prefix="/productos", tags=["productos"], responses={404: {"message": "Sin productos registrados."}})
router.mount("/static", StaticFiles(directory="static"), name="static")
plantillas = Jinja2Templates(directory="plantillas")

@router.get("/", response_model=list[DatosProducto])
async def listaProductos():
    return productosEsquema(coleccionProductos.find())

@router.get("/nuevo_producto", response_class=HTMLResponse)
async def nuevoProducto(request: Request):
    return plantillas.TemplateResponse("p09.html", {"request": request})

@router.post("/nuevo_producto",response_model= DatosProducto ,status_code=201)
async def nuevoProducto(producto: DatosProducto):
    if type(buscarProducto("nombre", producto.nombre)) == DatosProducto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El producto ya existe")
    
    diccionario_producto = dict(producto)
    del diccionario_producto["id"]

    id = coleccionProductos.insert_one(diccionario_producto).inserted_id

    nuevo_producto = productosEsquema(coleccionProductos.find_one({"_id": id}))

    return DatosProducto((nuevo_producto))

@router.put("/editar_producto", response_model=DatosProducto)
async def user(producto: DatosProducto):
        producto_diccionario = dict(producto)
        del producto_diccionario["id"]

        try:
            coleccionProductos.find_one_and_replace({"_id": ObjectId(producto.id)}, producto_diccionario)
        except:
            return {"error": "No se ha actualizado el producto."}
        
        return buscarProducto("_id", ObjectId(producto.id))

@router.delete("/eliminar_producto/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminarProducto(id: str):
    encontrado = coleccionProductos.find_one_and_delete({"_id": ObjectId(id)})

    if not encontrado:
        return {"error": "No se ha encontrado el producto."}

def buscarProducto(field: str, key):
    try:
        producto = coleccionProductos.find_one({field: key})
        return DatosProducto(productosEsquema(producto))
    except:
        return {"error": "No se ha encontrado producto."}