import uvicorn
from fastapi import FastAPI
from Routers import autenticacion

app = FastAPI()

app.include_router(autenticacion.router)

#RUTA DE LA BASE DE DATOS
#mongodb+srv://Plantium:Plantium@cluster0.yxlgbor.mongodb.net/?retryWrites=true&w=majority

if __name__ == "__main__":
    uvicorn.run(app)