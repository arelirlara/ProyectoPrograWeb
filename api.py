import uvicorn
from fastapi import FastAPI
from Routers import autenticacion, catalogo, usuario
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(autenticacion.router)
app.include_router(catalogo.router)
app.include_router(usuario.router)

# Configurar los orígenes permitidos en CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    # Agrega aquí otros orígenes permitidos
]

# Habilitar el middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
