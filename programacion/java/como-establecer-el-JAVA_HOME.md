# Guia para establecer la variable JAVA_HOME

Hay varios programas, IDE, servicios, o incluso si se instala un JDK no por las vias por defecto, que pueden no funcionar sin esta variable de entorno, puesto que la buscan para saber donde esta el binario del JDK; otro caso comun es cuando hay varias versiones del JDK instalado, y un programa equis no sabe cual usar, y esta variable es la que lo dicta, y de eso va esta guia.

## Como hacerlo:

1. Asegurate de tener un JDK instalado, puedes guiarte por [aqui](como-instalar-jdk-21.md), en ese caso la guia se centra en el JDK-21, puesto que no viene siempre en los paquetes por defecto de algunos Ubuntu, pero es valida para cualquier version, solo hay que cambiar el numero (8, 11, 17, 21, 23).

2. En los casos en los que se quiere cambiar la version por defecto del JDK del sistema se usa:
   ```sh
   sudo update-alternatives --config java
   ```

   - Se te pedira elegir la version entre las que esten instaladas

3. Para que la variable se inicie en el arranque del sistema hay que escribirla en el `/etc/environment`, agregas al final del archivo algo asi:

   ```sh
   # o la que sea la ruta de tu version deseada
   JAVA_HOME="/usr/lib/jvm/java-21-oracle-x64" 
   PATH="$PATH:$JAVA_HOME/bin"
   ```

   - Para aplicar el cambio inmediatamente debes ejecutar:

     ```sh
     source /etc/environment
     ```

4. Verifica que se haya guardado con 

   ```sh
   echo $JAVA_HOME
   ```

   