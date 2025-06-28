# Posible error en API Manager 4.x.x al usar certificados oficiales, o sea no autogenerados
Normalmente a los certificados autogenerados le ponemos un comodin en la CA, mas varias entradas en el SAN, sin embargo en uno (de Let's Encrypt por ejemplo) oficial no es asi, puesto que no se le debe configurar Localhost como uno de los SAN por temas de seguridad. Esto trae consigo que cuando el APIM le tire a sus endpoints internos les tire, por ejemplo, a `https://localhost:9443/services/` mientras que nuestro APIM se llama `is.prod.com`, dara una excepcion similar a esta:
```logs
ERROR {org.apache.catalina.core.ContainerBase.[Catalina].[localhost].[/publisher].[idp]}  
Servlet.service() for servlet [idp] threw exception:  
javax.net.ssl.SSLHandshakeException: No subject alternative DNS name matching localhost found
```
Aqui lo que esta pasando es que el APIM en su comunicacion interna usa el hostname configurado en el `deployment.toml` en **internal_hostname**, el cual por defecto es siempre `localhost` por lo que en un entorno fuera del local debemos declararlo, empezando asi con el primer paso para **solucionar el problema**: 
1. Agregar a las configuraciones del `deployment.toml` el campo de **internal_hostname**
```toml
[server]
hostname = "is.prod.com"
internal_hostname = "is.prod.com" # nombre con el que se comunicara internamente
node_ip = "$env{NODE_IP}"
offset = 0
# ...
```
2. En el `/etc/hosts` agrega el nombre que configuraste en el `hostname` con la ip local
```c
127.0.0.1 localhost 
# <ip_address> <hostname>
# ejemplo: 
is.prod.com 127.0.0.1
```
3. Por defecto las webapps vienen configuradas para intercomunicarse con localhost, asi que se debe modificar este comportamiento en los siguientes archivos:
   * **Publisher path**: repository/deployment/server/webapps/publisher/site/public/conf/settings.json.
   * **Admin portal path**: repository/deployment/server/webapps/admin/site/public/conf/settings.json. 
   * **Devportal path**: repository/deployment/server/webapps/devportal/site/public/theme/settings.json`
```json
app: {
...,
 origin: {
    host: 'is.prod.com', // aqui iba localhost
 },
...
```
[^1]
En teoria esto ya deberia completar el proceso de configuracion del certificado en el APIM

[^1]: After you change the hostname, if you encounter login failures when trying to access the API Publisher and API Developer Portal with the error `Registered callback does not match with the provided url`, see ['Registered callback does not match with the provided url' error](https://apim.docs.wso2.com/en/4.2.0/troubleshooting/troubleshooting-invalid-callback-error) in the Troubleshooting guide.
