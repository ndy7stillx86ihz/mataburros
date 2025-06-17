### Instalación de uv

PENDIENTE**
### Creación de un proyecto utilizando las tecnologías SQLAlchemy, Fastapi y Alembic con el gestor uv.

Crear un directorio para el proyecto
``` 
mkdir nombre_del_directorio
```

Creación de un entorno virtual

```
python3 -m venv .venv
```
Activación del entorno virtual

```
source .venv/bin/activate
```

Inicializar el proyecto con uv

```
uv init
```

Instalar Fastapi 

```
uv add fastapi
```

Instalar la versión CLI de Fastapi

```
uv add "fastapi[standard]"
```

Instalar SQLAlchemy

```
uv add sqlalchemy==2.0.23
```

Instalar Alembic

```
uv add alembic==1.13.1
```