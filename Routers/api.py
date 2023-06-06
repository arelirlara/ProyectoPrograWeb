from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from esquemas.esquemas import DatosAutenticacion, DatosProducto, productosEsquema, DatosSucursales, sucursalesEsquema
from bson import ObjectId
from DB.DB import coleccion
from DB.DB import coleccionProductos
from DB.DB import coleccionSucursales

router = APIRouter(prefix="/tulip", tags=["tulip"])
router.mount("/static", StaticFiles(directory="static"), name="static")
plantillas = Jinja2Templates(directory="plantillas")

#FUNCIONES ----------------------------------------------------------------
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
        return {"id": str(producto["_id"]),
            "nombre": str(producto["nombre"]),
            "descripcion": str(producto["descripcion"]),
            "precio": str(producto["precio"]),
            "imagen": str(producto["imagen"])}
    except:
        return {"error": "No se ha encontrado producto."}

def buscarSucursal(field: str, key):
    try:
        sucursal = coleccionSucursales.find_one({field: key})
        return DatosSucursales(sucursalesEsquema(sucursal))
    except:
        return {"error": "No se ha encontrado sucursal."}
#--------------------------------------------------------------------------------

#MÉTODO PARA OBTENER LOS PRODUCTOS TANTO COMO USUARIO Y ADMINISTRADOR
@router.get("/login/success/productos", response_model=list[DatosProducto])
async def listaProductos():
    return productosEsquema(coleccionProductos.find())

#MÉTODO PARA OBTENER LOS PRODUCTOS TANTO COMO USUARIO Y ADMINISTRADOR
@router.get("/login/success/sucursales", response_model=list[DatosSucursales])
async def listaSucursales():
    return sucursalesEsquema(coleccionSucursales.find())

#MÉTODOS DE LA INTERFAZ USUARIO ---------------------------------------------------------------------------------------------
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
#---------------------------------------------------------------------------------------------------------------------------

#MÉTODOS PARA AUTENTICACIÓN ----------------------------------------------------------------------------------------------
@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return plantillas.TemplateResponse("login.html", {"request": request})

@router.post("/login/success", response_class=HTMLResponse)
async def enviarFormulario(request: Request, datosFormulario: DatosAutenticacion = Depends(DatosAutenticacion.as_form)):
    usuarioAdmin = buscarUsuario(datosFormulario.usuario, datosFormulario.contrasena)
    if not usuarioAdmin:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticación inválidas.")
    
    return plantillas.TemplateResponse("catalogo_administrador.html", {"request": request})
#---------------------------------------------------------------------------------------------------------------------------

#MÉTODOS DE LA INTERFAZ ADMINISTRADOR -----------------------------------------------------------------------------------
@router.get("/login/success/catalogo", response_class=HTMLResponse)
async def catalogoAdministrador(request: Request):
    return plantillas.TemplateResponse("catalogo_administrador.html", {"request": request})

@router.get("/login/success/contacto", response_class=HTMLResponse)
async def contactoAdministrador(request: Request):
    return plantillas.TemplateResponse("contacto_administrador.html", {"request": request})
#---------------------------------------------------------------------------------------------------------------------------

#MÉTODOS ADMINISTRADOR PARA "CREAR", "EDITAR" O "ELIMINAR" PRODUCTO ----------------------------------------------------
@router.get("/login/success/productos/nuevo_producto", response_class=HTMLResponse)
async def nuevoProducto(request: Request):
    return plantillas.TemplateResponse("nuevo_producto_administrador.html", {"request": request})

@router.post("/login/success/productos/crear_producto", response_class=HTMLResponse)
async def crearProducto(request: Request):
    form_data = await request.form()
    
    nombre_producto = form_data.get('inputNombre')
    descripcion_producto = form_data.get('inputDescripcion')
    precio_producto = form_data.get('inputPrecio')
    imagen_producto = form_data.get('inputURLImagen')
    
    producto = {
        "nombre": nombre_producto,
        "descripcion": descripcion_producto,
        "precio": precio_producto,
        "imagen": imagen_producto
    }

    coleccionProductos.insert_one(producto)

    return plantillas.TemplateResponse("catalogo_administrador.html", {"request": request})

@router.get("/login/success/productos/editar_producto/{id}", response_class=HTMLResponse)
async def editarProducto(request: Request, id: str):
    encontrado = buscarProducto("_id", ObjectId(id))
    if not encontrado:
        return {"error": "No se ha encontrado el producto."}
    return plantillas.TemplateResponse("editar_producto_administrador.html", {"request": request, "_id": id, "nombre": encontrado['nombre'], "descripcion": encontrado['descripcion'], "precio": encontrado['precio'], "imagen": encontrado['imagen']})

@router.post("/login/success/productos/modificar_producto/{id}", response_class=HTMLResponse)
async def actualizarElemento(id: str, request: Request):
    form_data = await request.form()
    
    nombre_producto = form_data.get('inputNombre')
    descripcion_producto = form_data.get('inputDescripcion')
    precio_producto = form_data.get('inputPrecio')
    imagen_producto = form_data.get('inputURLImagen')
    
    producto_modificado = {
        "nombre": nombre_producto,
        "descripcion": descripcion_producto,
        "precio": precio_producto,
        "imagen": imagen_producto
    }

    coleccionProductos.find_one_and_replace({"_id": ObjectId(id)}, producto_modificado)
    return plantillas.TemplateResponse("catalogo_administrador.html", {"request": request})

@router.delete("/login/success/productos/eliminar_producto/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminarProducto(id: str):
    encontrado = coleccionProductos.find_one_and_delete({"_id": ObjectId(id)})

    if not encontrado:
        return {"error": "No se ha encontrado el producto."}
#---------------------------------------------------------------------------------------------------------------------------

#MÉTODOS ADMINISTRADOR PARA "CREAR", "EDITAR" O "ELIMINAR" SUCURSAL ----------------------------------------------------
@router.get("/login/success/sucursales/nueva_sucursal", response_class=HTMLResponse)
async def nuevaSucursal(request: Request):
    return plantillas.TemplateResponse("nueva_sucursal_administrador.html", {"request": request})

@router.post("/login/success/sucursales/crear_sucursal", response_class=HTMLResponse)
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

    return plantillas.TemplateResponse("contacto_administrador.html", {"request": request})

@router.put("/login/success/sucursales/editar_sucursal/{id}", response_model=DatosSucursales)
async def user(sucursal: DatosSucursales):
        sucursal_diccionario = dict(sucursal)
        del sucursal_diccionario["id"]

        try:
            coleccionSucursales.find_one_and_replace({"_id": ObjectId(sucursal.id)}, sucursal_diccionario)
        except:
            return {"error": "No se ha actualizado el producto."}
        
        return buscarSucursal("_id", ObjectId(sucursal.id))

@router.delete("/login/success/sucursales/eliminar_sucursal/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminarSucursal(id: str):
    encontrado = coleccionSucursales.find_one_and_delete({"_id": ObjectId(id)})

    if not encontrado:
        return {"error": "No se ha encontrado la sucursal."}
#---------------------------------------------------------------------------------------------------------------------------