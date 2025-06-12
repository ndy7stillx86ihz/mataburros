keytool -genkey -keyalg RSA -alias wso2am -keystore wso2carbon.jks -storepass wso2carbon -validity 360 -keysize 2048
-dname "CN=Apimanager, OU=SBS NA, O=BCC Inc, L=Habana, S=Habana, C=CU" -ext san=ip:192.0.135.169

keytool -export -alias wso2am -keystore wso2carbon.jks -storepass wso2carbon -file am.pem

keytool -import -alias wso2am -file am.pem -keystore client-truststore.jks -storepass wso2carbon