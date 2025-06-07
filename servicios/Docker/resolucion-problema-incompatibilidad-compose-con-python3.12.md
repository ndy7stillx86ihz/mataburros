# Resolución del problema de incompatibilidad de Docker Compose (v1), con las librerías de Python 3.12

## Descripción del problema

Actualmente casi todas las últimas versiones de los sistemas GNU/Linux vienen ya por defecto con **Python** **3.12**. **Docker Compose v1,** el cual se instala por defecto, por ejemplo en sistemas basados **Debian** al usar el gestor de paquetes por defecto, **APT**, para instalar docker, depende de Python, específicamente de la librería **distutils**, la cual no está en esa version, en los binarios, por defecto, o sea:
```console
~$ apt install docker.io docker-compose
```

## Resolución

Hay varias vías para resolver esto:

1. **Actualizar** la instalación de **Docker Compose** a v2, de la misma forma que en la forma anterior, pero usando otra version.
    1. En los Releases de Github descarga la ultima version (o al menos una estable) para tu sistema operativo, es un binario executable.
    2. Copia el binario para la ruta `~/.docker/cli-plugins/docker-compose` (nota que **docker-compose** es como debe llamarse el binario destino), crea las carpetas si no existen.
    3. Asignale permisos de ejecucion al binario con `chmod +x`.
    
    En Debian se haria el proceso completo asi:
    ```sh
    wget https://github.com/docker/compose/releases/download/v2.37.0/docker-compose-linux-x86_64 && \
    mkdir -p ~/.docker/cli-plugins && \
    mv docker-compose-linux-x86_64 ~/.docker/cli-plugins/docker-compose && \
    chmod +x ~/.docker/cli-plugins/docker-compose && \
    systemctl restart docker # opcional
    ```

2. Crearse un entorno virtual (demasiado tedioso) con Venv, UV, Poetry o cualquier otro, en lo personal no soporto los entornos virtuales, así que ésta ni la considero.

3. Bajar la versión de Python3, máximo a la 3.10.

4. Contenerizar el propio Docker Compose 
    Asumo que tienes **Docker** instalado, así que puedes usar Docker Compose contenerizado, copia y pega este codigo en tu consola, y cuando uses el comando `docker-compose <arg> <arg>` funcionará tal cual esperabas del normal:

   ```bash
   VERSION="1.29.2" && \
   docker pull docker/compose:$VERSION && \
   echo "alias docker-compose='docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v \"\$PWD:\$PWD\" -w \"\$PWD\" docker/compose:$VERSION'" >> ~/.bashrc && \
   source ~/.bashrc && \
   docker-compose version
   ```

   * Las desventajas de usar esta alternativa es que es un poco más lenta.
   * La ventaja es que al menos garantiza que no dependerá de nada de tu SO.
