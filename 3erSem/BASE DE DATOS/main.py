from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Modelo de datos para el usuario
class User(BaseModel):
    name: str
    age: int

# "Base de datos" en memoria para guardar usuarios
users_db = []

# Ruta raíz
@app.get("/")
def home():
    return "Hello world!"

# Ruta con parámetro de path
@app.get("/users/{user_id}")
def read_user(user_id: int):
    return {"user_id": user_id}

# Ruta con parámetros de consulta
@app.get("/search")
def search(q: str, limit: int = 10):
    return {"query": q, "limit": limit}

# Ruta para crear un usuario (POST)
@app.post("/users")
def create_user(user: User):
    users_db.append(user.model_dump())
    return {"message": f"Usuario {user.name} creado", "data": user}

# Ruta para listar todos los usuarios
@app.get("/users")
def list_users():
    return users_db