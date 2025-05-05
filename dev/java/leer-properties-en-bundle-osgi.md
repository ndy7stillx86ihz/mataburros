# Como leer un archivo de **properties** en un Bundle OSGI

En un bundle OSGi (por ejemplo, en WSO2 Identity Server o cualquier entorno OSGi en general), si tienes un archivo `.properties` ubicado en `src/main/resources`, al compilarse el bundle ese archivo se empaqueta en el classpath (en el JAR). Por lo tanto, puedes acceder a él usando el **classloader**.

Para leer estos resources siempre dentro de mi paquete de **utils** creo la clase `PropertiesLoader` :

```java
package org.sample.bundle.project.impl.utils;

import org.apache.commons.logging.Log;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

public class PropertiesLoader {
    private static Log log;

    public static Properties loadProperties(String fileName) {
        Properties props = new Properties();
        try (InputStream input = PropertiesLoader.class.getClassLoader().getResourceAsStream(fileName)) {
            if (input == null) {
                if (log != null)
                    log.error("Archivo no encontrado: " + fileName);
                return props;
            }
            props.load(input);
        } catch (IOException e) {
            if (log != null)
                log.error("Error de lectura: " + fileName, e);
        }
        return props;
    }

    public static void setLogger(Log log) {
        PropertiesLoader.log = log;
    }
}
```

Un ejemplo de uso de esta es:
```java
...
PropertiesLoader.setLogger(log); // logger (opcional)
Properties props = PropertiesLoader.loadProperties("sample.properties");

final String URI = props.getProperty("BaseUri"); // uri prop
NotifyAMLOnLoginUseCase notifier = new NotifyAMLOnLoginUseCase(URI);
...

```

## OJO

* El archivo `.properties` debe estar directamente en `src/main/resources`, o bien debes usar la ruta relativa correcta si está en un subdirectorio (por ejemplo, `"config/app.properties"`).

* Dentro de un entorno OSGi, esta técnica funciona siempre que el recurso esté empaquetado dentro del JAR y no sea excluido por error del `build`.