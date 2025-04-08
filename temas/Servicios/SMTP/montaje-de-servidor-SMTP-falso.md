# Montando servidor SMTP falso

Para ésta entrada se usará la app del ya cerrado repo de GitHub: **[FakeSMTP](https://github.com/Nilhcem/FakeSMTP)**, un servidor SMTP falso, open source, escrito en Java, lo cual lo hace **multiplataforma**, con GUI tanto para escritorio como para servirlo en la propia CLI.

![img](https://camo.githubusercontent.com/597f8bedaa17cce4ac5b1f26097f1d322143cd0e56b82888fa052cbfdd86c523/687474703a2f2f6e696c6863656d2e6769746875622e696f2f46616b65534d54502f696d616765732f73637265656e73686f745f6d61632e706e67)

## Procedimiento

### Requisitos Previos

JVM >= 1.6 instalado en la PC para ejecutarlo.

Apache Maven 3 al menos para compilar.

---

1. Descargar/clonar el repo de GitHub:

   ```sh
   git clone https://github.com/Nilhcem/FakeSMTP;
   cd FakeSMTP
   ```

2. Dentro de la carpeta descargada, ejecuta:

   ```sh
   mvn package
   ```

   - Si quieres saltarte los tests agrega al final: `-Dmaven.test.skip` (no recomendable).
   - Este comando creara un `.jar` en la carpeta si todo sale bien.

### Como usarlo

Para el funcionamiento basico, usando la GUI, navega a la carpeta `target/` donde se habra compilado el programa y ejecutalo:

```sh
java -jar fakeSMTP-2.1-SNAPSHOT.jar
```

Para especificar donde se guardaran los correos (en general el output del programa) usa la opcion `-o` o `--output-dir` \<dir\>:

```sh
java -jar fakeSMTP-VERSION.jar -o output_directory_name
java -jar fakeSMTP-VERSION.jar --output-dir output_directory_name
```

Si quieres autoarrancar el server, sin GUI, y en puerto y hostearlo en una direccion diferente,:

```sh
java -jar fakeSMTP-VERSION.jar -s -b -p 2525 -a 172.16.0.1
java -jar fakeSMTP-VERSION.jar --start-server --background --port 2525 --bind-address 127.0.0.1
```

Si no quieres guardarlos en el sistema y prefieres dejarlos en memoria usa:
```sh
java -jar fakeSMTP-VERSION.jar -m
```

Para ver las demas funcionalidades, mas una guia mas detallada usa `--help`:

```sh
java -jar fakeSMTP-VERSION.jar --help
```

#### Docker

Luego de compilar el codigo en el paso 2, usaremos el `Dockerfile` que esta en la propia carpeta del proyecto, se puede usar de dos formas:

##### 1. Como contenedor, como un servicio unico:

```sh
docker run -it -d --privileged=true -v /home/fakesmtp/mail:/output -p 2525:25 fakesmtp
```

- En ese comando se pone por defecto un usuario privilegiado
- Se mapea el puerto `25` del contenedor al `2525` del host
- la carpeta de `/home/fakesmtp/mail` se mapea a la de `/output` del contnedor

##### 2. Sirviendolo como un servicio mas, dentro de un contenedor usando `docker-compose`:

- En el `compose.yml` que tengas de la aplicacion que depende del servicio de correo, agrega en `services` algo asi:

  ```yaml
  version: "3.9"
  
  networks:
      app_network:
          driver: bridge
  volumes:
  	...
      fakesmtp_received:
  
  services:
  	# tu app con sus configuraciones
      app:
      	...
          depends_on:
              - email
      # el FakeSMTP
      email:
          build:
              context: relative/route/to/FakeSMTP
              dockerfile: Dockerfile
          ports:
              - "2525:25"
          volumes:
              - fakesmtp_received:/output
          networks:
              - app_network
  
  ```

  > Recuerda configurar tu app para que consuma del servicio `email`