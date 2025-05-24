import org.apache.commons.logging.Log;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

public class BundlePropertiesLoader {

    private static Log log;

    public static Properties loadProperties(String fileName) {
        Properties props = new Properties();
        try (InputStream input = BundlePropertiesLoader.class.getClassLoader().getResourceAsStream(fileName)) {
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
        BundlePropertiesLoader.log = log;
    }
}

