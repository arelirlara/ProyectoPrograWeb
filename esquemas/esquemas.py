from fastapi import Form
from pydantic import BaseModel

class DatosGenerales(BaseModel):
    id: str | None
    nombre: str

#USUARIOS ADMINISTRADOR
class DatosAutenticacion(BaseModel):
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

#PRODUCTOS
class DatosProducto(DatosGenerales):
    descripcion: str
    precio: str
    imagen: str

    @classmethod
    def form_producto(
        cls,
        nombre: str = Form(...),
        descripcion: str = Form(...),
        precio: str = Form(...),
        imagen: str = Form(...),
    ):
        return cls(
            nombre=nombre,
            descripcion=descripcion,
            precio = precio,
            imagen = imagen,
        )

def productoEsquema(producto) -> dict:
    return {"id": str(producto["_id"]),
            "nombre": str(producto["nombre"]),
            "descripcion": str(producto["descripcion"]),
            "precio": str(producto["precio"]),
            "imagen": str(producto["imagen"])}

def productosEsquema(productos) -> list:
    return [productoEsquema(producto) for producto in productos]

#SUCURSALES
class DatosSucursales(DatosGenerales):
    telefono: str
    celular: str
    direccion: str
    urlMaps: str

    @classmethod
    def form_sucursal(
        cls,
        nombre: str = Form(...),
        telefono: str = Form(...),
        celular: str = Form(...),
        direccion: str = Form(...),
        urlMaps: str = Form(...)
    ):
        return cls(
            nombre=nombre,
            telefono=telefono,
            celular = celular,
            direccion = direccion,
            urlMaps = urlMaps
        )

def sucursalEsquema(sucursal) -> dict:
    return {"id": str(sucursal["_id"]),
            "nombre": str(sucursal["nombre"]),
            "telefono": str(sucursal["telefono"]),
            "celular": str(sucursal["celular"]),
            "direccion": str(sucursal["direccion"]),
            "urlMaps": str(sucursal["urlMaps"])}

def sucursalesEsquema(sucursales) -> list:
    return [sucursalEsquema(sucursal) for sucursal in sucursales]