**Distribución de los directorios de Alembic**

```plaintext
.
├──dir_alembic/
│   ├──env.py
│   └──script.py.mako
└──versions/
```

- **dir_alembic/** --> directorio del env de migraciones.
- *env.py* --> sciprt usado cada vez que alembic hace la conexión con la Base de Datos.
- *script.py.mako* --> plantilla que permite la generación de alembic de script para nuevas migraciones.
- **versions/** --> todos los scripts creados para migraciones.

>  **Aclaración**: para ejecutar cualquier comando de alembic debe desplazarse hasta el directorio donde se encuentre el fichero `alembic.ini`

**Comandos frecuentes:**

* Nombre  del último script de migración aplicado. 

`````
alembic current
`````

* Orden en que fueron aplicados los script para las migraciones.
```
alembic history
```

*base --> primer script 
(head) --> último*

* Sincronización de la Base de Datos con los modelos de SQl Alchemy actuales.

```
alembic revision --autogenerate -m "mensaje"
```

El script generado debe revisarse para quedarse solo con los cambios requeridos para la generación e inversión de un cambio.

* Script de migración más reciente disponible 

```
alembic heads
```

* Aplicar un script de migración 

    - más reciente

    ```
    alembic upgrade head
    ```

    - uno específico

    ```
    alembic upgrade nombre_del_script
    ```

