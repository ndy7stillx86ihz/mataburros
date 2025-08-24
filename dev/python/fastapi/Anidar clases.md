
A veces se necesita devolver dos objetos de clases diferentes en una response, si ese es tu caso pues a continuación se explicará cómo anidar clases en Fastapi.

*Para esta explicación se utilizará el como ejemplo obtener un rol, por tanto hay que obtener los permisos asociados al rol. Y cuyas clases que generan las tablas poseen una relación de muchos a muchos nombrada **permisos** en la clase Role y nombrada  **rol_relacion** en la clase Permiso.

Se define la clase de response para Permiso con los atributos del modelo

``` python
class PermissionsResponse(BaseModel):  
    nombre: Optional[str] = Field(default=None)  
    nombre_visual: Optional[str] = Field(default=None)  
    id: int  
  
    class Config:  
        from_attributes = True
```

Se define la clase de response para Role con los atributos del modelo y con el atributo permiso del tipo Permiso (*en este caso es una lista ya que un rol puede tener tanto 0 como muchos permisos, si fuese una relación de uno a uno no sería una lista de elementos sino un solo objeto).

``` python
class RoleGET(BaseModel):  
    rol: str = Field(..., max_length=40, min_length=1)  
    descripcion: Optional[str] = Field(None, max_length=100)  
    id: int  
    permission_list: List[PermissionsResponse] = Field(None)
```

Se define la función para obtener el rol.

``` python
def get_role(db: Session, id_rol: int):  
"""
Encuentra un rol en y lo devuelve con sus permisos.
Args:
	db: sesión actual de la Base de Datos.
	id_rol: id del rol en la tabla rol de la Base de Datos.

"""
    role_query =  select(
	    Role
    ).where(
	    Role.id == id_rol
	    )  
	role = db.scalars(role_query).first()
	if not role:
		raise HTTPException(  
	    status_code=HTTP_404_NOT_FOUND,  
	    detail=" El rol no existe")
    permisos = role.permisos if role.permisos else None  
    role_response = RoleGET(  
        id = role.id,  
        rol = role.rol,  
        descripcion = role.descripcion,  
        permission_list = permisos  
    )  
    return role_response
```

El endpoint

``` python
@router.get("/{id}", response_model=RoleGET)  
async def get_role_endpoint(  
        id: int,    
        db: Session = Depends(get_db)  
):  
    return get_role(db, id)
```






