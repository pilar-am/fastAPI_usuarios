from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from schema.usuario_schema import UsuarioSchema, DatosUsuario
from config.db import engine
from model.usuario import usuarios
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List

usuario = APIRouter()

@usuario.get("/")
def root():
    return {"mensaje": "Hola, soy Fastapi desde router"}

@usuario.post("/api/usuario", status_code=HTTP_201_CREATED)
def crear_usuario(data_usuario:UsuarioSchema):
    with engine.connect() as conn:
        new_usuario = data_usuario.model_dump()
        #Encriptar contraseña
        new_usuario["contrasenya"] = generate_password_hash(data_usuario.contrasenya, "pbkdf2:sha256:30", 30)
        #print(new_usuario)
        conn.execute(usuarios.insert().values(new_usuario))
        conn.commit()
        return Response(status_code=HTTP_201_CREATED)

@usuario.get("/api/usuario", response_model=List[UsuarioSchema])
def get_usuarios():
    with engine.connect() as conn:
        result = conn.execute(usuarios.select()).fetchall()

        # Obtener los nombres de las columnas
        columns = usuarios.columns.keys()

        # Convertir el resultado a una lista de diccionarios
        user_list = [dict(zip(columns, row)) for row in result]

        return user_list
       
@usuario.get("/api/usuario/{usuario_id}", response_model=UsuarioSchema)
def get_usuario(usuario_id: str):
    with engine.connect() as conn:
        result = conn.execute(usuarios.select().where(usuarios.c.id == usuario_id)).first()
        return result

@usuario.put("/api/usuario/{usuario_id}")   # Me da un error pero me actualiza la BD
def update_usuario(data_update:UsuarioSchema, usuario_id: str):

    with engine.connect() as conn:
        encript_password = generate_password_hash(data_update.contrasenya, "pbkdf2:sha256:30", 30)
        usuario_actualizado = { usuarios.c.nombre: data_update.nombre,
                                usuarios.c.username: data_update.username,
                                # usuarios.c.id: data_update.id,
                                usuarios.c.contrasenya: encript_password
                            }
        
        #Actualizando la BD
        conn.execute(usuarios.update().values(usuario_actualizado).where(usuarios.c.id == usuario_id))
        conn.commit()
        
        # Recoge el usuario actualizado para devolverlo
        result = conn.execute(usuarios.select().where(usuarios.c.id == usuario_id)).first()

        return result


@usuario.delete("/api/usuario/{usuario_id}", status_code=HTTP_204_NO_CONTENT)
def delete_usuario(usuario_id: str):
    with engine.connect() as conn:
        usuario_id_int = int(usuario_id)
        delete_statement = usuarios.delete().where(usuarios.c.id == usuario_id_int)
        # print("SQL Statement DELETE:", delete_statement)
        conn.execute(delete_statement)
        conn.commit()

        return Response(status_code=HTTP_204_NO_CONTENT)

@usuario.post("/api/usuario/login", status_code=200)
def login(datos_usuario: DatosUsuario):
    with engine.connect() as conn:
        result = conn.execute(usuarios.select().where(usuarios.c.username == datos_usuario.username)).first()
        print(result)

        if result != None:
            # result[3]  es porque está en la 4 posición (id, nombre, username, contrasenya)
            check_password = check_password_hash(result[3], datos_usuario.contrasenya)
            print(check_password)
            if check_password:
                return {
                    "status": 200,
                    "message": "Logueado con éxito"
                }
            
        return {
            "status": HTTP_401_UNAUTHORIZED,
            "message": "Acceso denegado"
        }
    
