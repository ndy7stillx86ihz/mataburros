# Como instalar Java JDK 21 en Debian

## Via APT

1. Actualizar paquetes: ```sudo apt update```
2. Instalar el JDK por defecto: ```sudo apt install default-jdk```
3. Instalar el JDK-21: ```sudo apt install openjdk-21*``` (no siempre funciona)
4. Verificar version: `java -version`

## Via Oracle con un Debian Package

1. Descargar el **.deb**: `wget https://download.oracle.com/java/21/latest/jdk-21_linux-x64_bin.deb`
2. Instalar: `sudo dpkg -i jdk-21_linux-x64_bin.deb`
3. Verificar instalacion: `java -version`