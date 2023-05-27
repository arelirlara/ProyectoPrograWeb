import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from Routers import usuario, sucursales

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(usuario.router)
app.include_router(sucursales.router)

if __name__ == "__main__":
    uvicorn.run(app)