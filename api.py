import uvicorn
from fastapi import FastAPI
from Routers import autenticacion

app = FastAPI()

app.include_router(autenticacion.router)

if __name__ == "__main__":
    uvicorn.run(app)