import uvicorn
from fastapi import FastAPI
from Routers import autenticacion, catalogo, usuario
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(autenticacion.router)
app.include_router(catalogo.router)
app.include_router(usuario.router)

if __name__ == "__main__":
    uvicorn.run(app)