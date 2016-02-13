from base import Pagina, Usuario
from flask_sqlalchemy import SQLAlchemy

me = Usuario('miNombre', 'MiUsuario', 'MiContrasena', 'Micorreo')
db.session.add(me)
db.session.commit()