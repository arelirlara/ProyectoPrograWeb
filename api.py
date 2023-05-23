import uvicorn
from fastapi import FastAPI
from Routers import autenticacion, catalogo, sucursales

app = FastAPI()

app.include_router(autenticacion.router)
app.include_router(catalogo.router)
app.include_router(sucursales.router)

if __name__ == "__main__":
    uvicorn.run(app)