# Resolución del problema de incompatibilidad de Docker Compose (v1), con las librerías de Python 3.12

## Descripción del problema

Actualmente casi todas las últimas versiones de los sistemas GNU/Linux vienen ya por defecto con **Python** **3.12**. **Docker Compose v1,** el cual se instala por defecto, por ejemplo en sistemas basados **Debian** al usar el gestor de paquetes por defecto, **APT**, para instalar docker, depende de Python, específicamente de la librería **distutils**, la cual no está en esa version, en los binarios, por defecto, o sea:
```console
~$ apt install docker.io docker-compose
```

## Resolución

Hay varias vías para resolver esto:

0. **Instalar la versión oficial del Release en github, no la de APT:**

   1. Primero asegúrate de borrar la de tu OS:

      ```console
      ~$ apt purge docker-compose
      ```

   2. Descargar el binario en alguna carpeta que pertenezca al [**$PATH**](https://en.wikipedia.org/wiki/PATH_(variable)), copia y pega el script:

      ```bash
      sudo curl -L "https://github.com/docker/compose/releases/download/v1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
      sudo chmod +x /usr/local/bin/docker-compose && \
      docker-compose --version
      ```

1. **Actualizar** la instalación de **Docker Compose** a v2, de la misma forma que en la forma anterior, pero usando otra version.

2. Crearse un entorno virtual (demasiado pesado) con Venv, UV, Poetry o cualquier otro, en lo personal no soporto los entornos virtuales, así que ésta ni la considero.

3. Bajar la versión de Python3, máximo a la 3.10.

4. Asumo que tienes **Docker** instalado, así que puedes usar Docker Compose contenerizado, copia y pega este codigo en tu consola, y cuando uses el comando `docker-compose <arg> <arg>` funcionará tal cual esperabas del normal:

   ```bash
   VERSION="1.29.2" && \
   docker pull docker/compose:$VERSION && \
   echo "alias docker-compose='docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v \"\$PWD:\$PWD\" -w \"\$PWD\" docker/compose:$VERSION'" >> ~/.bashrc && \
   source ~/.bashrc && \
   docker-compose version
   ```

   * Las desventajas de usar esta alternativa es que es un poco más lenta.
   * La ventaja es que al menos garantiza que no dependerá de nada de tu SO.

