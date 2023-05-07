import uvicorn
from fastapi import FastAPI
from Routers import autenticacion, catalogo

app = FastAPI()

app.include_router(autenticacion.router)
app.include_router(catalogo.router)

if __name__ == "__main__":
    uvicorn.run(app)