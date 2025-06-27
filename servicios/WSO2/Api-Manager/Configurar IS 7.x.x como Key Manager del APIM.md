
1. Primero es necesario tener un certificado y una PK
2. Usando un certificado existente, crear una Keystore con ese certificado, y la PK en formato PKCS12
```sh
openssl pkcs12 -export -in <certificate file>.crt -inkey <private>.key -name "<alias>" -certfile <additional certificate file> -out <pfx keystore name>.pfx
```
3. (Opcional) Convertir a formato JKS
```sh
keytool -importkeystore -srckeystore <pkcs12 file name>.pfx -srcstoretype pkcs12 -destkeystore <JKS name>.jks -deststoretype JKS
```

4. Importar el certificado tambien a la Trustore del servidor