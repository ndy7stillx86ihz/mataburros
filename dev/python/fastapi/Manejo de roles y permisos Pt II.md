## Manejo de roles y permisos Pt II

### Poblar la tabla para los permisos al iniciar el servidor de Fastapi

* Creación de un diccionario para almacenar todos los permisos del sistema

*Este diccionario me gusta nombrarlo scopes, donde cada key es el nombre del permiso que asignó a un usuario para acceder a una funcionalidad y cada value es el nombre visual para el usuario. Cada permiso corresponde a una funcionalidad requerida por un endpoint, ejemplo: listar municipios como permiso requerido en el endpoint para listar municipios*

``` python
scopes = {
	"name": "name_visual"
}
```

* Creación de la función para insertar en los permisos en la tabla para permisos

``` python
def insert_permissions_db(permissions_for_users: dict[str], db: Session):  
    """  
    Inserta en la tabla permiso los permisos definidos en el diccionario
    para el sistema, con su nombre visual para el usuario final.   
	     Args:        
			permissions_for_users: dict[str] -> permisos del sistema.
			db: sesión actual de la Base de Datos.    
	"""
    for permission, name_permission in permissions_for_users.items():  
	    query_search_permission = select(Permission).where(
	    Permission.nombre == permission
	    )  
        result_query_search_permission =db.scalars(
        query_search_permission
        ).first()  
        if not result_query_search_permission:  
            permission_db = Permission(  
                nombre = permission,  
                nombre_visual= name_permission.title()  
            )  
            db.add(permission_db)  
            db.commit()   
```

**En el archivo main.py**

*Recordar realizar las importaciones del diccionario scopes y la función insert_permissions_db*

* Importar el decorador async context manager

``` python
from contextlib import asynccontextmanager
```

* Creación de la función asíncrona para ejecutar la función insert_permissions_db cuando inicie el servidor
``` python
@asynccontextmanager  
async def lifespan(app: FastAPI):  
    db = SessionLocal()  
    insert_permissions_db(scopes, db)  
    yield  
    db.close()
```

db --> db crea una sesión para establecer conexión con la BD.

* Asiganar al parámetro lifespan, de la app de Fastapi, la función asíncrona definida

``` python
app = Fastapi(
	# todos los parámetros que necesites definir
	lifespan = lifespan
)
```

