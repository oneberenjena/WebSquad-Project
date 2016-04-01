import unittest, time, re
from base import db, Usuario, Pagina, Contacto, Grupo, Membresia, Publicacion, Hilo, Foro, PaginaSitio

class WebSquadUnittest(unittest.TestCase):
	def setUp(self):
		pass

	def test_registro(self):
		# db.create_all()
		# userTest = Usuario(nombre="benjaPrueba", username="benjaUser", contrasena="benjaPasswd", correo="benja@mail.com")
		db.session.add(Usuario(nombre="benjaPrueba", username="benjaUserNew222", contrasena="benjaPasswd", correo="benja222@mail.com"))
		# db.session.commit()
		failed=False
		try:
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			db.session.flush() 
			failed=True

		userQuery = Usuario.query.filter_by(username = "benjaUserNew222").first()

		# Probando que se agrego el usuario correctamente
		if (userQuery.nombre == "benjaPrueba"):
			testResult = True
		elif (not userQuery or userQuery.nombre != "benjaPrueba"):
			testResult = False
			print("Failed at testing for register")
		
		self.assertTrue(testResult)
		db.session.delete(userQuery)
		db.session.commit()

	def test_modifPagina(self):
		db.create_all()
		# userTest = Usuario(nombre="benjaPrueba", username="benjaUser4", contrasena="benjaPasswd", correo="benja4@mail.com")
		db.session.add(Usuario(nombre="benjaPrueba", username="benjaUser8", contrasena="benjaPasswd", correo="benja8@mail.com"))

		failed=False
		try:
		   db.session.commit()
		except Exception as e:
		   db.session.rollback()
		   db.session.flush() 
		   failed=True

		userQuery = Usuario.query.filter_by(username = "benjaUser8").first()
		
		# Probando que se agrego el usuario correctamente
		if (userQuery.nombre == "benjaPrueba"):
			testResult = True
		elif (not userQuery or userQuerynombre != "benjaPrueba"):
			testResult = False
			print("Failed at testing for page modify")
		self.assertTrue(testResult)

		# userPag = Pagina(usuario_id = userTest.idUsuario, usuario = userTest)
		db.session.add(Pagina(usuario_id = userQuery.idUsuario, usuario = userQuery))
		# db.session.commit()
		failed=False
		try:
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			db.session.flush() 
			failed=True

		# Probando que se agrego la pagina correctamente
		userPagQuery = Pagina.query.filter_by(usuario_id = userQuery.idUsuario).first()


		if (userPagQuery.usuario == userQuery):
			testResult = True
		elif (not userPagQuery or userPagQuery.usuario != userQuery):
			testResult = False
			print("Failed at testing for page modify")
		self.assertTrue(testResult)

		#Probando que se modifica bien	
		userPagQuery.titulo = "titulo de prueba benjaPrueba"
		userPagQuery.contenido = "contenido de prueba benjaPrueba"
		# db.session.commit()
		failed=False
		try:
		   db.session.commit()
		except Exception as e:
		   db.session.rollback()
		   db.session.flush() 
		   failed=True

		userPagQuery2 = Pagina.query.filter_by(usuario_id = userQuery.idUsuario).first()

		if (userPagQuery2.usuario_id == userPagQuery.usuario_id):
			if (userPagQuery2.titulo == "titulo de prueba benjaPrueba"
				and userPagQuery2.contenido == "contenido de prueba benjaPrueba"):
				testResult = True
			elif(not userPagQuery2 or userPagQuery2.titulo != "titulo de prueba benjaPrueba"
				or userPagQuery2.contenido != "contenido de prueba benjaPrueba"):
				testResult = False
				print("Failed at testing for page modification of: ", userQuery.nombre)
		self.assertTrue(testResult)

		db.session.delete(userQuery)
		db.session.delete(userPagQuery)
		db.session.delete(userPagQuery2)
		db.session.commit()
	
	def test_newContact(self):
		db.session.add(Usuario(nombre="benja2",username="benjTest2",contrasena="benjPasswd",correo="benjMail2@mail.com"))
		db.session.add(Usuario(nombre="benja2.0",username="benjTest22.0",contrasena="benjPasswd2.0",correo="benjMail22.0@mail.com"))
		failed=False
		try:
		   db.session.commit()
		except Exception as e:
		   db.session.rollback()
		   db.session.flush() 
		   failed=True

		userTest1 = Usuario.query.filter_by(username="benjTest2").first()
		userTest2 = Usuario.query.filter_by(username="benjTest22.0").first()

		# Verificando que los usuarios fueron bien agregados
		if (userTest1.username == "benjTest2" and userTest2.username == "benjTest22.0"):
			testResult = True
		else:
			testResult = False
			print("Failed at testing for user contact add")
		self.assertTrue(testResult)

		db.session.add(Contacto(usuario1=userTest1.idUsuario, usuario2=userTest2.idUsuario))
		failed=False
		try:
		   db.session.commit()
		except Exception as e:
		   db.session.rollback()
		   db.session.flush() 
		   failed=True
		# Verificando que la relacion fue bien creada
		
		contactTest = Contacto.query.filter_by(usuario1=userTest1.idUsuario, usuario2=userTest2.idUsuario).first()

		if (contactTest.usuario1 == userTest1.idUsuario and
			contactTest.usuario2 == userTest2.idUsuario):
			testResult = True
		elif (not contactTest or contactTest.usuario1 != userTest1.idUsuario or
			contactTest.usuario2 != userTest2.idUsuario):
			testResult = False
			print("Failed at testing for user contact add")
		self.assertTrue(testResult)

		db.session.delete(userTest1)
		db.session.delete(userTest2)
		db.session.delete(contactTest)
		db.session.commit()

	def test_createGrupoAndMembresia(self):
		db.session.add(Usuario(nombre="benja2",username="benjTest9",contrasena="benjPasswd",correo="benjMail9@mail.com"))
		db.session.add(Usuario(nombre="benja2.0",username="benjTest9.0",contrasena="benjPasswd2.0",correo="benjMail9.0@mail.com"))
		failed=False
		try:
		   db.session.commit()
		except Exception as e:
		   db.session.rollback()
		   db.session.flush() 
		   failed=True

		userTest1 = Usuario.query.filter_by(username="benjTest9").first()
		userTest2 = Usuario.query.filter_by(username="benjTest9.0").first()

		# Verificando que los usuarios fueron bien agregados
		if (userTest1.username == "benjTest9" and userTest2.username == "benjTest9.0"):
			testResult = True
		else:
			testResult = False
			print("Failed at testing for user membership add")
		self.assertTrue(testResult)

		# Se crea grupo
		db.session.add(Grupo(nombre='webSquadMVP1'))
		failed=False
		try:
		   db.session.commit()
		except Exception as e:
		   db.session.rollback()
		   db.session.flush() 
		   failed=True

		group = Grupo.query.filter_by(nombre='webSquadMVP1').first()

		if (not group):
			testResult = False
			print("Failed to create group")
		else:
			testResult = True
		self.assertTrue(testResult)

		# Se crea membresia 
		db.session.add(Membresia(es_admin=True, usuario=userTest1, idGrupo = group.idGrupo))
		db.session.add(Membresia(es_admin=False, usuario=userTest2, idGrupo = group.idGrupo))
		failed=False
		# db.session.commit()
		try:
		   db.session.commit()
		except Exception as e:
		   db.session.rollback()
		   db.session.flush() 
		   failed=True

		memb1 = Membresia.query.filter_by(usuario=userTest1).first()
		memb2 = Membresia.query.filter_by(usuario=userTest2).first()

		# Correctitud de la membresia
		
		if (memb1.usuario.username == 'benjTest9' and
			memb2.usuario.username == 'benjTest9.0'):
			testResult = True
		elif (not memb1 or not memb2 or memb1.usuario.username != 'benjTest9'
			or memb2.usuario.username != 'benjTest9.0'):
			testResult = False
			print("Failed at testing for user membership add")
		self.assertTrue(testResult)		

		db.session.delete(userTest1)
		db.session.delete(userTest2)
		db.session.delete(memb1)
		db.session.delete(memb2)
		db.session.delete(group)
		db.session.commit()


	def test_newPublicacion(self):
		db.session.add(Usuario(nombre="benjaPrueba", username="benjaOP", contrasena="benjaPasswd", correo="benjaop@mail.com"))
		# db.session.commit()
		failed=False
		try:
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			db.session.flush() 
			failed=True

		userQuery = Usuario.query.filter_by(username = "benjaOP").first()

		# Probando que se agrego el usuario correctamente
		if (userQuery.nombre == "benjaPrueba"):
			testResult = True
		elif (not userQuery or userQuery.nombre != "benjaPrueba"):
			testResult = False
			print("Failed at testing for register")
		
		self.assertTrue(testResult)

		# Probando la publicacion
		db.session.add(Publicacion(titulo='miPublicacion', contenido='blablablablabla',autor_id = userQuery.idUsuario, tipo='nueva'))

		failed=False
		try:
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			db.session.flush() 
			failed=True

		# Verificacion de su agregacion:
		
		newPubl = Publicacion.query.filter_by(titulo='miPublicacion').first()

		if (newPubl.autor_id == userQuery.idUsuario and newPubl.titulo == 'miPublicacion' and
			newPubl.contenido == 'blablablablabla'):
			testResult = True
		elif(not newPubl or (newPubl.autor_id != userQuery.idUsuario or newPubl.titulo != 'miPublicacion' or
			newPubl.contenido != 'blablablablabla')):
			testResult = False
			print("Failed to test publication")
		self.assertTrue(testResult)

		db.session.delete(userQuery)
		db.session.delete(newPubl)
		db.session.commit()

	def test_newHilo(self):
		db.session.add(Usuario(nombre="benjaPrueba", username="benjaOP", contrasena="benjaPasswd", correo="benjaop@mail.com"))
		# db.session.commit()
		failed=False
		try:
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			db.session.flush() 
			failed=True

		userQuery = Usuario.query.filter_by(username = "benjaOP").first()

		# Probando que se agrego el usuario correctamente
		if (userQuery.nombre == "benjaPrueba"):
			testResult = True
		elif (not userQuery or userQuery.nombre != "benjaPrueba"):
			testResult = False
			print("Failed at testing for register")
		
		self.assertTrue(testResult)

		# Probando la publicacion
		db.session.add(Publicacion(titulo='miPublicacion', contenido='blablablablabla',autor_id = userQuery.idUsuario, tipo='nueva'))

		failed=False
		try:
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			db.session.flush() 
			failed=True

		# Verificacion de su agregacion:
		
		newPubl = Publicacion.query.filter_by(titulo='miPublicacion').first()

		if (newPubl.autor_id == userQuery.idUsuario and newPubl.titulo == 'miPublicacion' and
			newPubl.contenido == 'blablablablabla'):
			testResult = True
		elif(not newPubl or (newPubl.autor_id != userQuery.idUsuario or newPubl.titulo != 'miPublicacion' or
			newPubl.contenido != 'blablablablabla')):
			testResult = False
			print("Failed to test publication")
		self.assertTrue(testResult)

		# Crear el hilo
		
		db.session.add(Hilo(titulo='nuevoHilo', pubRaiz_id = newPubl.idPublicacion,pubRaiz = newPubl,tipo = 1))

		failed=False
		try:
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			db.session.flush() 
			failed=True

		# Verificar
		newHilo = Hilo.query.filter_by(pubRaiz = newPubl).first()
		
		if (newHilo.titulo == 'nuevoHilo' and newHilo.pubRaiz_id == newPubl.idPublicacion):
			testResult = True
		elif (not newHilo or (newHilo.titulo != 'nuevoHilo' or newHilo.pubRaiz_id != newPubl.idPublicacion)):
			testResult = False
			print("Failed to test thread of publication")
		self.assertTrue(testResult) 

		db.session.delete(userQuery)
		db.session.delete(newPubl)
		db.session.delete(newHilo)
		db.session.commit()

	# def test_newForo(self):
	# 	db.session.add(Usuario(nombre="benjaPrueba", username="benjaOP1", contrasena="benjaPasswd", correo="benjaop1@mail.com"))
	# 	# db.session.commit()
	# 	failed=False
	# 	try:
	# 		db.session.commit()
	# 	except Exception as e:
	# 		db.session.rollback()
	# 		db.session.flush() 
	# 		failed=True

	# 	userQuery = Usuario.query.filter_by(username = "benjaOP1").first()

	# 	# Probando que se agrego el usuario correctamente
	# 	if (userQuery.nombre == "benjaPrueba"):
	# 		testResult = True
	# 	elif (not userQuery or userQuery.nombre != "benjaPrueba"):
	# 		testResult = False
	# 		print("Failed at testing for register")
		
	# 	self.assertTrue(testResult)

	# 	# CREACION DEL FORO
	# 	db.session.add(db.Foro(titulo='foroWebSquad', autor_id = userQuery.idUsuario))

	# 	failed=False
	# 	try:
	# 		db.session.commit()
	# 	except Exception as e:
	# 		db.session.rollback()
	# 		db.session.flush() 
	# 		failed=True

	# 	# VERIFICACION
		
	# 	newForum = Foro.query.filter_by(titulo = 'foroWebSquad').first()

	# 	if (not newForum):
	# 		testResult = False
	# 		print("Failed to test forum")
	# 	elif (newForum.autor_id == userQuery.idUsuario):
	# 		testResult = True
	# 	self.assertTrue(testResult)

	# 	db.session.delete(userQuery)
	# 	db.session.delete(newForum)
	# 	db.commit()
	
	def test_newSitePage(self):
		db.session.add(PaginaSitio(url='http://webSquad.com'))
		failed=False
		try:
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			db.session.flush() 
			failed=True

		# VERIFICACION
		
		newSite = PaginaSitio.query.filter_by(url= 'http://webSquad.com').first()

		if (newSite):
			testResult = True
		else:
			testResult = False
			print("Failed to test site")
		self.assertTrue(testResult)

		db.session.delete(newSite)
		db.session.commit()

	def tearDown(self):
		pass

if __name__ == "__main__":
	unittest.main(verbosity=2)
