from pydantic import BaseModel
from typing import Optional

class UsuarioSchema(BaseModel):
    id: Optional[int]
    nombre:str
    username:str
    contrasenya:str

class DatosUsuario(BaseModel):
    username: str
    contrasenya: str