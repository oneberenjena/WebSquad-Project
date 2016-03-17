from base import *
db.create_all()

db.session.add(Usuario(nombre="David",username="david",contrasena="12345678",correo="david@aa.com"))
db.session.add(Usuario(nombre="Norelys",username="norelys",contrasena="12345678",correo="norelys@aa.com"))
db.session.add(Usuario(nombre="Andres",username="andres",contrasena="12345678",correo="rocha@aa.com"))

db.session.commit()