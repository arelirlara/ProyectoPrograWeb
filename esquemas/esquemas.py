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
    imagen_id: str

def productoEsquema(producto) -> dict:
    return {"id": str(producto["_id"]),
            "nombre": str(producto["nombre"]),
            "descripcion": str(producto["descripcion"]),
            "precio": str(producto["precio"]),
            "imagen_id": str(producto["imagen"])}

def productosEsquema(productos) -> list:
    return [productoEsquema(producto) for producto in productos]

#SUCURSALES
class DatosSucursales(DatosGenerales):
    telefono: str
    celular: str
    direccion: str
    urlMaps: str

def sucursalEsquema(sucursal) -> dict:
    return {"id": str(sucursal["_id"]),
            "nombre": str(sucursal["nombre"]),
            "telefono": str(sucursal["telefono"]),
            "celular": str(sucursal["celular"]),
            "direccion": str(sucursal["direccion"]),
            "urlMaps": str(sucursal["urlMaps"])}

def sucursalesEsquema(sucursales) -> list:
    return [sucursalEsquema(sucursal) for sucursal in sucursales]