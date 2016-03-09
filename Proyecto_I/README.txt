#Instrucciones para ejecutar esta aplicación bajo Linux 
#(para otros sistemas , por favor consultar la documentación de Flask)
#Necesitará tener instalado pip3
#Si no lo tiene instalado, puede hacerlo ejecutando el comando
sudo apt-get install python3-pip

#Crear una carpeta aplicaciones

mkdir aplicaciones

#En una ventana de comandos cambiar a la carpeta principal de la aplicación.

cd aplicaciones

Crear el ambiente virtual

pyvenv-3.4 --without-pip --system-site-packages venv3

#Descomprimir los archivos de esta distribución

#Activar el ambiente virtual

source venv3/bin/activate

#Instalar Flask (La primera vez que lo haga puede que necesite ejecutarlo con sudo)

pip3 install flask

#instalar la gestión de opciones del servidor web  (La primera vez que lo haga puede que necesite ejecutarlo con sudo)

sudo pip3 install flask-script

#Ejecutar la aplicación

python base.py runserver

#El servidor quedará ejecutando indefinidamente.
#Puede abrir en un navegador la dirección
# http://127.0.0.1:5000/ para entrar en la aplicación.

#Para detener el servidor 
#escribir Ctrl-c en la cónsola en la que ejecuta el servidor.

#Cuando la aplicación ya está instalada y se quiere descargar de 
#cohesión una nueva versión puede hacerlo con los pasos siguientes.
#Respaldar la versión anterior

tar czvf ../SocialFl`date +%y%m%d%H%M%S`.tgz {static,base.py,app,README.txt}

#borrar la versión ya respaldada

rm -rf {static,base.py,app,README.txt}

#Descargar una nueva versión desde cohesión y 
#desempaquetarla en la carpeta de la aplicación

unzip socialFL.zip

#Ejecutar la aplicación

python base.py runserver

Si va a utilizar SQLAlchemy verifique que este paquete está instalado. Si no
es el caso pruebe ejecutando los siguientes comandos de instalación:

sudo pip3 install SQLAlchemy
sudo pip3 install Flask-SQLAlchemy
sudo pip3 install Flask-Migrate

Para verificar si ya están instalados ejecute python3 una consola de terminal e importe 
los archivos pertinentes:

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

Para instalar con Miniconda:
Crear ambiente:

conda create -n condaenv3 python=3.4
source activate condaenv3

Instalar paquetes

conda install flask
conda install --channel https://conda.anaconda.org/ziff flask-script
conda install --channel https://conda.anaconda.org/hugo flask-sqlalchemy
(Flask-Migrate no está empaquetado para anaconda)