# UUID en Java

La manera más sencilla de generar un UUID (Universally Unique Identifier) es mediante la clase `randomUUID` del paquete `java.util.UUID`

El código concreto es:

```java
String uuid = java.util.UUID.randomUUID().toString();
```

También podemos crearnos un método estático que nos los devuelva como una cadena sin formato ni caracteres que no sean número y letras

```java
public static final String uuid() {
    String result = java.util.UUID.randomUUID().toString();

    result.replaceAll("-", "");
    result.substring(0, 32);

    return result;
}
```
