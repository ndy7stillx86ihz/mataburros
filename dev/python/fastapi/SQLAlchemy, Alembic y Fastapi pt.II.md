Configurar las rutas del proyecto en el archivo main.py

```
from fastapi import FastAPI

#Importar los endpoints

#Importar el settings
from app.core.config import get_settings

app = FastAPI(
	title="",
	description="",
	version="",
	openapi_url=f"{settings.API_V1_STR}/openapi.json",  
	docs_url=f"{settings.API_V1_STR}/docs",  
	redoc_url=f"{settings.API_V1_STR}/redoc",
)

#incluir cada router de los endpoints
app.include_router(auth.router, prefix=settings.API_V1_STR)

#definir lo que expone la ruta raíz 
@app.get("/")  
def read_root():
	pass
```

**Endpoint**

Configuración de una ruta para un endpoint

```
from fastapi import APIRouter

router = APIRouter(
		prefix="/nombre_de_las_rutas", 
		tags=["nombre_de_la_agrupación"]
)
```

Definición de los decoradores para las peticiones HTTP

```
@router.post(path)
```