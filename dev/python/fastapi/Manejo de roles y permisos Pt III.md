## Manejo de roles y permisos Pt III

*Se  utiliza **autorización** por **contraseña** usando **token Bearer** en este caso, por ello, se necesita en cada endpoint que requiera permiso obtener el usuario actual con los permisos que posee y verificar que se/an lo/s necesario/s. Si desea realizar alguna verificación como si el token actual se encuentra en blacklist (ya que expiró o se desloguearon con él), depende de su definición de tablas y de las consultas que desea hacer. En este caso solo se hacen verificaciones del usuario y de los permisos que posee. Debe definir la **SECRET_KEY** y **ALGORITHM** (con el algoritmo utilizado para firmar el token) que utilizará. Importar el diccionario de los permisos*

* Creación de la función para obtener el usuario por id

``` python
def query_existence(db: Session, id_object: int, class_model):  
    """  
    Verifica la existencia de un objeto en la Base de Datos
    mediante el atributo id.    
    Params:        
	    class_model: clase de ORM que corresponde a una tabla 
	    de la Base de Datos.
	    id_object: id del objeto que se verificará.db: sesión actual 
	    de la Base de Datos.
	Returns:        
		query_select : object | None -> objeto encontrado 
					   en la Base de Datos.    
	""" 
	   
	select_object = select(class_model).where(class_model.id == id_object)  
    query_select = db.scalars(select_object).first()  
    if not query_select:  
        raise HTTPException(  
            status_code = HTTP_404_NOT_FOUND,  
            detail = f"{class_model.__name__} id: {id_object} no existe"        )  
    return query_select
```

* Importar las librerías necesarias

``` python
from fastapi.security import SecurityScopes
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from jose import jwt
```

jose -> manejo de jwt. 
Session -> 
Depends -> inyección de dependencias.


* Obtener el usuario actual

``` python
async def get_current_user(  
        security_scopes: SecurityScopes, 
        token: Annotated[str, Depends(oauth2_scheme)], 
        db: Session = Depends(get_db)  
	):  
	"""
		Se asigna en la variable authenticate_value los permisos 
		presentes en el token.
		Decodifica el jwt con la SECRET_KEY y el ALGORITHM definido.
		Comprueba la existencia del usuario. Extrae los permisos del token. 
		Comprueba mediante SecurityScopes que cada permiso presente en 
		el token correspondan con los requeridos por el o los requeridos 
		por el endpoint. Se maneja la excepción cuando el token expira.  
		
	"""
	try:
	    authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'  
	    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  
	    user_id = payload.get("id")  
	    if query_existence(db, user_id, User) is None:  
	        raise HTTPException(  
	            status_code = HTTP_404_NOT_FOUND,  
	            detail = "El usuario no existe"  
	        )  
	    token_scopes = payload.get("scopes", [])  
	    for scope in security_scopes.scopes:  
	        if scope not in token_scopes:  
	            raise HTTPException(  
	                status_code=status.HTTP_403_FORBIDDEN,  
	                detail="Not enough permissions",  
	                headers={"WWW-Authenticate": authenticate_value},  
	            )  
	    return user_id
	except JWTError:  
	    raise HTTPException(  
	        status_code=status.HTTP_401_UNAUTHORIZED,  
	        detail="Acces token expired"  
	    )
```

**En el fichero para el endpoint importar el nombre de la clase bajo la cual se creó la tabla en la Base de Datos, el diccionario scopes, la librería Security y la función get_current_user**

* Asignar un permiso a un endpoint
*En este caso tomé de ejemplo una petición get*

``` python
@app.get("name_URL_endpoint")  
async def get_item_endpoint( 
	id: int,
    current_user: User = Security(get_current_user, scopes=["name_permission"]),
    db: Session = Depends(get_db)  
    ):  
    return create_item(db, id)
```

