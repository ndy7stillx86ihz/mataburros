Antes que nada es importante hacer un backup completo de la carpeta de `<WSO2HOME>/repository/resources/security`, y trabajar en un entorno aislado de esa salva, solo es necesario arrastrar al entorno en el que se este el `client-trustore.jks`.

## Pasos iniciales que se deben hacer en ambos servidores[^1]
Ya el APIM y el IS traen una keystore por defecto, `wso2carbon.jks` (el IS a partir de la version 7.1.0 usa PKCS12, o sea es `wso2carbon.p12`), estas deben ser sustituidas con Keystores nuevas, que contengan el/los certificado/s que se van a usar, normalmente se usa el mismo certificado tanto para el SSL del servidor, como para la intercomunicacion de los backends del servidor, no obstante es posible usar mas de un certificado para separar estas responsabilidades, **en esta solucion se usara el mismo para ambos.**

### Creando la Keystore

1. Crear Keystore a partir de un certificado usando PKCS12
```sh
openssl pkcs12 -export -in <certificate file>.crt -inkey <private>.key -name "<alias>" -out <pfx keystore name>.p12
```
2. Convertir a Java Keystore (JKS) de ser necesario
```sh
keytool -importkeystore -srckeystore <pkcs12 file name>.p12 -srcstoretype pkcs12 -destkeystore <JKS name>.jks -deststoretype JKS
```
3. Importar el root CA al keystore:
```sh
keytool -import -v -trustcacerts -alias ExternalCARoot -file AddTrustExternalCARoot.crt -keystore newkeystore.jks -storepass mypassword
```
### Importar certificados a la Truststore:

1. Exportar la clave publica de la keystore
```sh
keytool -export -alias certalias -keystore newkeystore.jks -file <public key name>.pem
```
2. Importar a la Truststore 
```sh
keytool -import -alias certalias -file <public key name>.pem -keystore client-truststore.jks -storepass wso2carbon
```

[^1]: Para revisar si se ejecutaron bien cualquiera de los siguientes pasos verifica las keystore (tanto la propia keystore como truststore) con el comando: 
	```sh
	keytool -v -list -keystore <keystore>.jks -storepass wso2carbon
	```
	
