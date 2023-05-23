from pymongo import MongoClient

cliente = MongoClient("mongodb+srv://Plantium:Plantium@cluster0.yxlgbor.mongodb.net/?retryWrites=true&w=majority")
db = cliente["Plantium"]
coleccion = db["users"]
coleccionProductos = db["products"]
coleccionSucursales = db["stores"]