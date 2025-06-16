# Agregar certificados de confianza al JDK

Hay situaciones en las que una request a un recurso externo nos da error 500 usando ciertos clientes HTTP, que no tienen por defecto configurado el confiar en cualquier certificado, o sea el `SSLHostnameVerify = false`,  o una Truststore autogestionada, como por ejemplo:
```java
	// no verificar el certificado
	sslContext.init(
			new KeyManager[0],
			new TrustManager[]{
					new DefaultTrustManager()},
			new SecureRandom()
	);
```
Por ejemplo el `RestClient`de Spring Framework 6 si hace esta verificacion del SSL, usando la TrustStore del JDK activo, por lo que si haces una request a un sitio con certificado autofirmado, o de una CA no reconocida recibiras un error algo asi:
```json
{ 
	"error": "I/O error on POST request for \"https://identity-factdev.novaguard.pro/oauth2/token\": PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target", 
	"status": 500, 
	"errorCode": null 
}
```
Para solucionarlo hay que importar el certificado del sitio que estamos solicitando al key manager del JDK:
1. **Primero hay que estar seguros de [tener establecida la variable de entorno `JAVA_HOME`](https://iluvstderr.github.io/?path=dev/java/como-establecer-el-JAVA_HOME.md)** 
2. Extraer el certificado del sitio: 
```sh
openssl s_client -connect example.com:443 -showcerts </dev/null | openssl x509 -outform pem > trustedcert.crt
```
3. Importar el certificado a la Keystore:
```sh
sudo keytool -importcert -alias mycert -file trustedcert.crt -keystore $JAVA_HOME/lib/security/cacerts -storepass changeit
```
4. Verifica que se haya importado:
```sh
keytool -list -keystore $JAVA_HOME/lib/security/cacerts -storepass changeit | grep mycert
```
