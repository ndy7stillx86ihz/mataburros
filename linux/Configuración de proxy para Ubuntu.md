/etc/environment

```
nano environment
```

``` 
http_proxy="http://user:contraseña@dominio:puerto"
HTTP_PROXY="http://user:contraseña@dominio:puerto"
https_proxy=""http://user:contraseña@dominio:puerto""
HTTPS_PROXY=""http://user:contraseña@dominio:puerto""
no_proxy="localhost,127.0.0.1"
NO_PROXY="localhost,127.0.0.1"
```

/etc/apt/apt.conf.d

```
nano proxy.conf
```

```
Acquire {
        HTTP::proxy "http://user:contraseña@dominio:puerto/";
        HTTPS::proxy "https://user:contraseña@dominio:puerto/";
}
```

> *Aclaración*: realizar las configuraciones en el navegador en caso de utilizar Firefox.

> Faltan las configuraciones para wget y para Docker.