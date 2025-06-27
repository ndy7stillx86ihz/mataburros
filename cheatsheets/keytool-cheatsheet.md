# JAVA Keytool Cheatsheet

> fck los certificados, los odio

## TrustStore y KeyStore

La única diferencia entre trustStores y keyStores es lo que almacenan:

- **trustStore**: certificados de otras partes con las que esperas comunicarte, o de Autoridades Certificadoras (CA) en las que confías para identificar a otras partes.
- **keyStore**: claves privadas y los certificados con sus correspondientes claves públicas.

## Cómo identificar una CA raíz?

- Los certificados raíz están autofirmados.
- Los certificados autofirmados tienen el mismo emisor y sujeto.
- El campo "CA" está establecido en true.

---

## Crear y generar

### Generar keystore con clave RSA

```bash
keytool -genkey -alias mydomain -keyalg RSA -keystore keystore.jks -keysize 2048
```

### Generar certificado autofirmado

```bash
keytool -genkey -keyalg RSA -alias selfsigned -keystore keystore.jks -storepass password -validity 360 -keysize 2048
```

### Crear CSR (Certificate Signing Request)

```bash
keytool -certreq -alias mydomain -keystore keystore.jks -file mydomain.csr
```

### Crear keystore en formato PKCS12 (más moderno)

```bash
keytool -genkeypair -alias mydomain -keyalg RSA -keysize 2048 -keystore keystore.p12 -storetype PKCS12
```

---

## Importar y exportar

### Importar certificado de CA raíz o intermedia

```bash
keytool -import -trustcacerts -alias root -file ca.crt -keystore keystore.jks
```

### Importar certificado firmado

```bash
keytool -import -alias mydomain -file mydomain.crt -keystore keystore.jks
```

### Importar cadena de certificados (intermedia + raíz)

```bash
cat intermedio.crt root.crt > cadena.crt
keytool -import -trustcacerts -alias mydomain -file cadena.crt -keystore keystore.jks
```

### Exportar certificado del keystore

```bash
keytool -export -alias mydomain -file mydomain.crt -keystore keystore.jks
```

> Por defecto, exporta en formato DER. Puedes convertir a PEM con OpenSSL:

```bash
openssl x509 -inform DER -in mydomain.crt -out mydomain.pem -outform PEM
```

---

## Verificar y listar

### Verificar un certificado suelto

```bash
keytool -printcert -v -file cert.crt
```

### Listar todas las entradas del keystore

```bash
keytool -list -v -keystore keystore.jks
```

### Mostrar detalles de una entrada por alias

```bash
keytool -list -v -keystore keystore.jks -alias mydomain
```

### Verificar certificados del truststore del JDK

```bash
keytool -list -v -keystore $JAVA_HOME/lib/security/cacerts -storepass changeit
```

---

## Eliminar entradas

### Eliminar por alias

```bash
keytool -delete -alias mydomain -keystore keystore.jks
```

---

## Contraseñas

### Cambiar contraseña del keystore

```bash
keytool -storepasswd -new nueva_clave -keystore keystore.jks
```

### Cambiar contraseña de la clave privada dentro del keystore

```bash
keytool -keypasswd -alias mydomain -keystore keystore.jks
```

> La contraseña debe proporcionarse en todos los comandos que acceden al contenido del keystore. Para dichos comandos, si no se proporciona la opción `-storepass` en la línea de comandos, se solicitará en un prompt

---

## Formatos de archivo

- `.jks`: Java KeyStore propietario de Oracle.
- `.p12` / `.pfx`: PKCS#12, estándar multiplataforma.
- `.crt` / `.cer`: Certificado en formato DER (binario) o PEM (texto base64).
- `.pem`: Certificado en texto plano Base64, con encabezado y pie `-----BEGIN CERTIFICATE-----`.

---

## Otras operaciones útiles

### Convertir JKS a PKCS12

```bash
keytool -importkeystore -srckeystore keystore.jks -destkeystore keystore.p12 -deststoretype PKCS12
```

### Ver detalles sin tener contraseña (si el certificado está suelto)

```bash
keytool -printcert -file cert.crt
```

### Especificar tipo de keystore (JKS vs PKCS12)

```bash
keytool -list -keystore keystore.p12 -storetype PKCS12
```

### Comparar un certificado contra el de una keystore
```sh
# para el .pem:
openssl x509 -in tu_certificado.pem -noout -modulus | openssl md5

# para el cert del keystore:
keytool -exportcert -alias tu_alias -keystore tu_keystore.jks -rfc | openssl x509 -noout -modulus | openssl md5
```
o:
```sh
diff <(openssl x509 -in tu_certificado.pem -noout -modulus | openssl md5) <(keytool -exportcert -alias tu_alias -keystore tu_keystore.jks -rfc | openssl x509 -noout -modulus | openssl md5)
```
---

## Información adicional

- El keystore/truststore predeterminado del JDK está en:

```bash
$JAVA_HOME/lib/security/cacerts
```

- La contraseña por defecto suele ser: `changeit`

---

## Alias

- Cada entrada en un keystore está identificada por un **alias**.
- Usar alias distintos para claves, CA intermedias y certificados raíz evita conflictos.

---

## Consejos

1. SIEMPRE HACERLE UN BACKUP A LA KEYSTORE ANTES DE REALIZAR CAMBIOS!
2. Usa `keytool -list` frecuentemente para verificar los contenidos.
3. Los certificados importados deben estar en orden: primero el certificado del servidor, luego cualquier intermedio, y al final la raíz (si no se confía por default).
