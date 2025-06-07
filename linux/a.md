lgunas ocasiones puede ser necesario ejecutar un script en segundo plano; ya sea porque tarde mucho en finalizar o porque el programa tiene que ejecutarse de forma indefinida y al mismo tiempo se quieren analizar sus salidas/salidas en tiempo real, o cuando, en el caso de conexiones remotas, por el motivo que sea, se pueda producir una desconexión.

Analizaremos 3 posibilidades (&, nohup y screen):

& + bg + fg
Si añadimos un ampersand (&) al final de un comando o de un script que queramos ejecutar, este se ejecutará en segundo plano.

$ ./my-shell-script.sh &
[1] 10233
Si ejecutamos un comando de la forma habitual (en primer plano o foreground) y, después de pasado un cierto tiempo, nos damos cuenta que hubiera sido mejor ejecutarlo en segundo plano o background, lo podemos hacer sin necesidad de tener que matar el proceso y volver a ejecutarlo de nuevo con el ampersand. Esto se hace presionando “CTRL+Z” para suspender la ejecución del comando actual, y después invocando el comando bg.

$ ./my-shell-script.sh
^Z
[2]+  Detenido                my-shell-script.sh
$ bg
[2]+ my-shell-script.sh &
Este proceso que acaba de pasar al segundo plano, también se puede volver al primer plano con el comando fg.

$ fg 2
my-shell-script.sh
nohup + &
Al finalizar una sesión en un terminal se envía un signal (SIGHUP) a todos los procesos que esté ejecutando nuestro usuario. Como resultado, dichos procesos se mueren (aunque les hayamos puesto & al final).

Para evitar esto utilizamos el comando nohup. Este comando hace que un proceso ignore la señal SIGHUP, y redirige la salida de nuestro script a un archivo nohup.out que es creado en el directorio actual.

$ nohup ./my-shell-script.sh &
Una buena practica sería redireccionar stdin, stdout y stderr. Básicamente, por dos razones: i) rastrear la salida de nuestro script en caso de producirse algún error, y ii) evitar problemas al terminar nuestra sesión ssh, si es que la ejecutamos en un servidor remoto.

$ nohup ./my-shell-script.sh > foo.out 2> foo.err < /dev/null &
Esta opción es muy útil cuando necesitamos ejecutar un proceso largo y no nos interesa saber nada de él hasta que finalice. Nos podemos desconectar, irnos, y regresar al día siguiente para analizar el resultado del proceso.

screen
Si invocamos un comando en segundo plano (usando nohup y &), este se ejecutará incluso después de que cerremos nuestra sesión. Pero, en ninguno de los casos anteriores, podemos conectarnos a la misma sesión otra vez y ver exactamente qué es lo que está pasando en la pantalla. Si esto es lo que nos interessa, deberemos usar el comando screen.

El primer paso será ejecutar el script como parámetro del comando screen.

$ screen ./my-shell-script.sh
Si después de ejecutar la línea anterior tecleamos “CTRL+A d”, el sistema nos separara de la sesión actual (en la que estamos ejecutando my-shell-script.sh) y nos retornará a la terminal a la espera de teclear un nuevo comando.

Llegados a este punto, podemos cerrar la sesión, irnos, regresar, iniciar una nueva sesión y recuperar la pantalla (screen) que está corriendo nuestro script. Para ello, invocaremos el comando screen con el parámetro -ls para obtener un listado de las sesiones actuales:

```
$ screen -ls
[detached from 1788.ttys000.milleniumfalcon]
A continuación, mediante el parámetro -r y el identificador de la sesión recuperamos la pantalla que necesitemos:

$ screen -r 1788.ttys000.milleniumfalcon
¿Qué opción usar?
Pues eso dependerá en cada caso. Habrá veces que con el ampersand será suficiente y otras en las que tenemos que optar por una opción diferente.

Si la ejecución se va a resolver en la misma sesión, lo mejor es usar el &.

Si la ejecución es larga y no necesitamos intervenir para nada hasta que haya acabado de ejecutarse el script, lo mejor será nohup.

Si la ejecución es larga y, durante su ejecución necesitamos reconectarnos a la sesión para ir controlando la ejecución, lo mejor será screen.


