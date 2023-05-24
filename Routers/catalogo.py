from fastapi import APIRouter, Request, Depends, HTTPException, status
from DB.DB import coleccionProductos
from esquemas.esquemas import DatosProducto, productosEsquema

router = APIRouter(prefix="/productos", tags=["productos"], responses={404: {"message": "Sin productos registrados."}})

@router.get("/", response_model=list[DatosProducto])
async def listaProductos():
    return productosEsquema(coleccionProductos.find())

@router.post("/nuevo",response_model= DatosProducto ,status_code=201)
async def nuevoProducto(producto: DatosProducto):
    if type(buscarProducto("nombre", producto.nombre)) == DatosProducto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El producto ya existe")
    
    diccionario_producto = dict(producto)
    del diccionario_producto["id"]

    id = coleccionProductos.insert_one(diccionario_producto).inserted_id

    nuevo_producto = productosEsquema(coleccionProductos.find_one({"_id": id}))

    return DatosProducto((nuevo_producto))

def buscarProducto(field: str, key):
    try:
        producto = coleccionProductos.find_one({field: key})
        return DatosProducto(productosEsquema(producto))
    except:
        return {"error": "No se ha encontrado producto."}