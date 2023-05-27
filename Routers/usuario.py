from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from esquemas.esquemas import DatosAutenticacion, DatosProducto, productosEsquema
from bson import ObjectId
from DB.DB import coleccion
from DB.DB import coleccionProductos

router = APIRouter(prefix="/tulip", tags=["tulip"])
router.mount("/static", StaticFiles(directory="static"), name="static")
plantillas = Jinja2Templates(directory="plantillas")

#FUNCIONES
def buscarUsuario(usuario: str, contrasena: str):
    usuarioEncontrado = coleccion.find_one({"usuario": usuario})
    if usuarioEncontrado is None:
        return False
    elif usuarioEncontrado["contrasena"] != contrasena:
        return False
    else:
        return True
    
def buscarProducto(field: str, key):
    try:
        producto = coleccionProductos.find_one({field: key})
        return DatosProducto(productosEsquema(producto))
    except:
        return {"error": "No se ha encontrado producto."}

#MÉTODOS PARA USUARIO    
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

#MÉTODOS PARA AUTENTICACIÓN
@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return plantillas.TemplateResponse("login.html", {"request": request})

@router.post("/login/success/catalogo", response_class=HTMLResponse)
async def enviarFormulario(request: Request, datosFormulario: DatosAutenticacion = Depends(DatosAutenticacion.as_form)):
    usuarioAdmin = buscarUsuario(datosFormulario.usuario, datosFormulario.contrasena)
    if not usuarioAdmin:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticación inválidas.")
    
    return plantillas.TemplateResponse("catalogo_administrador.html", {"request": request})

#MÉTODOS PARA VISUALIZAR LOS PRODUCTOS TANTO COMO USUARIO Y ADMINISTRADOR
@router.get("/login/success/productos", response_model=list[DatosProducto])
async def listaProductos():
    return productosEsquema(coleccionProductos.find())

#MÉTODOS ADMINISTRADOR
@router.get("/login/success/productos/nuevo_producto", response_class=HTMLResponse)
async def nuevoProducto(request: Request):
    return plantillas.TemplateResponse("p09.html", {"request": request})

@router.post("/login/success/productos/crear_producto")
async def crear_producto(request: Request):
    form_data = await request.form()
    
    nombre_producto = form_data.get('inputNombre')
    descripcion_producto = form_data.get('inputDescripcion')
    precio_producto = form_data.get('inputPrecio')
    
    producto = {
        "nombre": nombre_producto,
        "descripcion": descripcion_producto,
        "precio": precio_producto
    }

    coleccionProductos.insert_one(producto)

    return {"message": "Producto agregado correctamente"}

@router.put("/login/success/productos/editar_producto", response_model=DatosProducto)
async def user(producto: DatosProducto):
        producto_diccionario = dict(producto)
        del producto_diccionario["id"]

        try:
            coleccionProductos.find_one_and_replace({"_id": ObjectId(producto.id)}, producto_diccionario)
        except:
            return {"error": "No se ha actualizado el producto."}
        
        return buscarProducto("_id", ObjectId(producto.id))

@router.delete("/login/success/productos/eliminar_producto/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminarProducto(id: str):
    encontrado = coleccionProductos.find_one_and_delete({"_id": ObjectId(id)})

    if not encontrado:
        return {"error": "No se ha encontrado el producto."}