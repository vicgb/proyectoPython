#!/usr/bin/python


import sys
from subprocess import call
import os
from lxml import etree

#######################################################################################
###### funcion crear(n): para crear los ficheros *.qcow2 de diferencias y los de ######
######   especificación en XML de cada MV, así como los bridges virtuales que    ###### 
######                          soportan las LAN de                              ######
#######################################################################################

def crear(num):

	# Si no se introduce un segundo parametro utilizamos por defecto el valor de 2
	if len(sys.argv) == 2:
		num_serv = 2
	else:
		num = sys.argv[2]

	# Guardamos el numero de maquinas que se introduce como parametro
	if((int(num) >= 0) and (int(num) <= 5)):
		
		
		num_serv = int(num)
	
	else:
		# Si el parametro introducido no esta entre las posibilidades del programa mostramos mensaje de error.
		sys.exit("ERROR: Valor incorrecto del segundo parámetro")

	# Guardamos el numero de maquinas en un fichero para que el resto de funciones del script pueda acceder a ellas

	os.system("touch num_serv.txt")
	os.system("echo "+str(num_serv)+" > num_serv.txt")

	# por defecto se crean siempre lb y c1 y posteriormente se crearan los servidores correspondientes al numero introducido como parametro
	os.system('qemu-img create -f qcow2 -b cdps-vm-base-pf1.qcow2 lb.qcow2')
	os.system('cp plantilla-vm-pf1.xml lb.xml')
	os.system('qemu-img create -f qcow2 -b cdps-vm-base-pf1.qcow2 c1.qcow2')
	os.system('cp plantilla-vm-pf1.xml c1.xml')

	# configuracion de c1

	# Cargamos el fichero XML de c1 y obtenemos el nodo raíz
	tree = etree.parse('c1.xml')
	root = tree.getroot()

	# Guardamos en 'doc' el fichero XML que vamos a modificar
	doc = etree.ElementTree(root)
	# Buscamos la etiqueta name y la guardamos
	name = root.find("name")
	# Editamos name
	name.text = 'c1'
	# Buscamos la etiqueta /devices/disk/source y la guardamos 
	source_disk = root.find("./devices/disk/source")	
	# Editar ese valor de la etiqueta 
	source_disk.set("file", '/mnt/tmp/pf1/c1.qcow2')
	# Buscamos la etiqueta /devices/interfaces/source y la guardamos
	source_interface = root.find("./devices/interface/source")
	# Editamos la bridge de LAN1
	source_interface.set("bridge", 'LAN1')

	outFile = open('c1.xml', 'w')
	doc.write("outFile")

	os.system("rm c1.xml")
	os.system("mv outFile c1.xml")

	# configuracion de lb

	# Cargamos el fichero XML de lb y obtenemos el nodo raíz
	tree = etree.parse('lb.xml')
	root = tree.getroot()

	# Guardamos en 'doc' el fichero XML que vamos a modificar
	doc = etree.ElementTree(root)
	# Buscamos la etiqueta name y la guardamos
	name = root.find("name")
	# Editamos name
	name.text = 'lb'
	# Buscamos la etiqueta /devices/disk/source y la guardamos 
	source_disk = root.find("./devices/disk/source")	
	# Editar ese valor de la etiqueta 
	source_disk.set("file", '/mnt/tmp/pf1/lb.qcow2')
	# Buscamos la etiqueta /devices/interfaces/source y la guardamos
	source_interface = root.find("./devices/interface/source")
	# Editamos la bridge de LAN1
	source_interface.set("bridge", 'LAN1')

	# Guardamos la etiqueta devices para crear una nueva etiqueta interface para añadir LAN2  
	source_interface_2 = root.find("devices")
	# Creamos sub-instancias/sub-elementos de source_interface_2
	sub_interface_2 = etree.SubElement(source_interface_2, "interface", type='bridge')
	sub_source_2 = etree.SubElement(sub_interface_2, "source", bridge='LAN2')
	sub_model = etree.SubElement(sub_source_2, "model", type='virtio')

	outFile = open('lb.xml', 'w')
	doc.write("outFile")

	os.system("rm lb.xml")
	os.system("mv outFile lb.xml")

	# Imprimimos por pantalla una notificacion de que se han creado c1 y lb
	print("SE HAN CREADO C1 Y LB")

	if ((num_serv >= 1) and (num_serv <= 5)):

		# si el valor introducido no es cero deberemos crear s1
		os.system("qemu-img create -f qcow2 -b cdps-vm-base-pf1.qcow2 s1.qcow2")
		os.system("cp plantilla-vm-pf1.xml s1.xml")

		# Procedemos a cargar el fichero XML de s1 y obtener el nodo raiz
		tree = etree.parse('s1.xml')
		root = tree.getroot()

		# Guardamos en "doc" el fichero XML que vamos a modificar
		doc = etree.ElementTree(root)

		# Buscamos la etiqueta name y la guardamos
		name = root.find("name")
		# Editamos name
		name.text = 's1'
		# Buscamos la etiqueta /devices/disk/source y la guardamos 
		source_disk = root.find("./devices/disk/source")	
		# Editar ese valor de la etiqueta 
		source_disk.set("file", '/mnt/tmp/pf1/s1.qcow2')
		# Buscamos la etiqueta /devices/interfaces/source y la guardamos
		source_interface = root.find("./devices/interface/source")
		# Editamos la bridge de LAN1
		source_interface.set("bridge", 'LAN2')

		outFile = open('s1.xml', 'w')
		doc.write("outFile")

		os.system("rm s1.xml")
		os.system("mv outFile s1.xml")

		print("Se ha creado S1")

		# Para un parametro mayor que 1 deberemos crear ademas s2 mediante el mismo proceso
		if (num_serv >= 2):

			os.system("qemu-img create -f qcow2 -b cdps-vm-base-pf1.qcow2 s2.qcow2")
			os.system("cp plantilla-vm-pf1.xml s2.xml")

			# Procedemos a cargar el fichero XML de s2 y obtener el nodo raiz
			tree = etree.parse('s2.xml')
			root = tree.getroot()

			# Guardamos en "doc" el fichero XML que vamos a modificar
			doc = etree.ElementTree(root)

			# Buscamos la etiqueta name y la guardamos
			name = root.find("name")
			# Editamos name
			name.text = 's2'
			# Buscamos la etiqueta /devices/disk/source y la guardamos 
			source_disk = root.find("./devices/disk/source")	
			# Editar ese valor de la etiqueta 
			source_disk.set("file", 'mnt/tmp/pf1/s2.qcow2')
			# Buscamos la etiqueta /devices/interfaces/source y la guardamos
			source_interface = root.find("./devices/interface/source")
			# Editamos la bridge de LAN1
			source_interface.set("bridge", 'LAN2')

			outFile = open('s2.xml', 'w')
			doc.write("outFile")

			os.system("rm s2.xml")
			os.system("mv outFile s2.xml")

			print("Se ha creado S2")

		# Para un parametro mayor que 2 deberemos crear ademas s3 mediante el mismo proceso
		if (num_serv >= 3):	

			os.system("qemu-img create -f qcow2 -b cdps-vm-base-pf1.qcow2 s3.qcow2")
			os.system("cp plantilla-vm-pf1.xml s3.xml")

			# Procedemos a cargar el fichero XML de s3 y obtener el nodo raiz
			tree = etree.parse('s3.xml')
			root = tree.getroot()

			# Guardamos en "doc" el fichero XML que vamos a modificar
			doc = etree.ElementTree(root)

			# Buscamos la etiqueta name y la guardamos
			name = root.find("name")
			# Editamos name
			name.text = 's3'
			# Buscamos la etiqueta /devices/disk/source y la guardamos 
			source_disk = root.find("./devices/disk/source")	
			# Editar ese valor de la etiqueta 
			source_disk.set("file", '/mnt/tmp/pf1/s3.qcow2')
			# Buscamos la etiqueta /devices/interfaces/source y la guardamos
			source_interface = root.find("./devices/interface/source")
			# Editamos la bridge de LAN1
			source_interface.set("bridge", 'LAN2')

			outFile = open('s3.xml', 'w')
			doc.write("outFile")
			os.system("rm s3.xml")
			os.system("mv outFile s3.xml")

			print("Se ha creado S3")

		# Para un parametro mayor que 3 deberemos crear ademas s4 mediante el mismo proceso
		if (num_serv >= 4):	

			os.system("qemu-img create -f qcow2 -b cdps-vm-base-pf1.qcow2 s4.qcow2")
			os.system("cp plantilla-vm-pf1.xml s4.xml")

			# Procedemos a cargar el fichero XML de s4 y obtener el nodo raiz
			tree = etree.parse('s4.xml')
			root = tree.getroot()

			# Guardamos en "doc" el fichero XML que vamos a modificar
			doc = etree.ElementTree(root)

			# Buscamos la etiqueta name y la guardamos
			name = root.find("name")
			# Editamos name
			name.text = 's4'
			# Buscamos la etiqueta /devices/disk/source y la guardamos 
			source_disk = root.find("./devices/disk/source")	
			# Editar ese valor de la etiqueta 
			source_disk.set("file", '/mnt/tmp/pf1/s4.qcow2')
			# Buscamos la etiqueta /devices/interfaces/source y la guardamos
			source_interface = root.find("./devices/interface/source")
			# Editamos la bridge de LAN1
			source_interface.set("bridge", 'LAN2')

			outFile = open('s4.xml', 'w')
			doc.write("outFile")

			os.system("rm s4.xml")
			os.system("mv outFile s4.xml")

			print("Se ha creado S4")

		# Para un parametro igual a 5 deberemos crear ademas s5 mediante el mismo proceso
		if (num_serv == 5):	

			os.system("qemu-img create -f qcow2 -b cdps-vm-base-pf1.qcow2 s5.qcow2")
			os.system("cp plantilla-vm-pf1.xml s5.xml")

			# Procedemos a cargar el fichero XML de s5 y obtener el nodo raiz
			tree = etree.parse('s5.xml')
			root = tree.getroot()

			# Guardamos en "doc" el fichero XML que vamos a modificar
			doc = etree.ElementTree(root)

			# Buscamos la etiqueta name y la guardamos
			name = root.find("name")
			# Editamos name
			name.text = 's5'
			# Buscamos la etiqueta /devices/disk/source y la guardamos 
			source_disk = root.find("./devices/disk/source")	
			# Editar ese valor de la etiqueta 
			source_disk.set("file", '/mnt/tmp/pf1/s5.qcow2')
			# Buscamos la etiqueta /devices/interfaces/source y la guardamos
			source_interface = root.find("./devices/interface/source")
			# Editamos la bridge de LAN1
			source_interface.set("bridge", 'LAN2')

			outFile = open('s5.xml', 'w')
			doc.write("outFile")

			os.system("rm s5.xml")
			os.system("mv outFile s5.xml")

			print("Se ha creado S5")

	else:
		print("ERROR - PARAMETRO INVALIDO")	


	

#############################################################################################
######  funcion arrancar(n): arranca las maquinas virtuales y muestra su consola   ##########
#############################################################################################




def arrancar(maquina):

	# Si no introducimos parametro arrancamos todas las maquinas (numero especificado en funcion crear y guardado en fichero "num_serv.txt")
	if len(sys.argv) == 2:

		print ("Arrancando máquinas por defecto (c1 y lb)")

		# Leemos el contenido del fichero donde tenemos guardado el numero de servidores a crear introducidos en la orden "crear" y lo guardamos en una variable
		f = open("num_serv.txt", "r")
		num_serv = int(f.read())
		f.close()

		# Creamos los bridges a las dos redes virtuales
		os.system("sudo brctl addbr LAN1")
		os.system("sudo brctl addbr LAN2")
		os.system("sudo ifconfig LAN1 up")
		os.system("sudo ifconfig LAN2 up")

		# Arrancamos el gestor de maquinas virtuales
		os.system("HOME=/mnt/tmp sudo virt-manager")

		# Procedemos a arrancar las maquinas por defecto (c1 y lb)
		os.system("sudo virsh define c1.xml")
		os.system("sudo virsh start c1")

		os.system("sudo virsh define lb.xml")
		os.system("sudo virsh start lb")

		# Lanzamos c1 y lb en terminales separados
		os.system("xterm -rv -sb -rightbar -fa monospace -fs 10 -title 'c1' -e 'sudo virsh console c1' &")
		os.system("xterm -rv -sb -rightbar -fa monospace -fs 10 -title 'lb' -e 'sudo virsh console lb' &")

		if ((num_serv >= 1) and (num_serv <= 5)):


			#  Repetimos el proceso de arranque con s1
			os.system("sudo virsh define s1.xml")
			os.system("sudo virsh start s1")
			os.system("xterm -rv -sb -rightbar -fa monospace -fs 10 -title 's1' -e 'sudo virsh console s1' &")

			print("Maquina S1 arrancada.")

			# Si el parametro es superior a 1 arrancaremos s2
			if(num_serv >= 2):

				# Repetimos el proceso de arranque con s3
				os.system("sudo virsh define s2.xml")
				os.system("sudo virsh start s2")
				os.system("xterm -rv -sb -rightbar -fa monospace -fs 10 -title 's2' -e 'sudo virsh console s2' &")

				print("Maquina S2 arrancada.")

			# Si el parametro es superior a 2 arrancaremos s3
			if(num_serv >= 3):

				# Repetimos el proceso de arranque con s3
				os.system("sudo virsh define s3.xml")
				os.system("sudo virsh start s3")
				os.system("xterm -rv -sb -rightbar -fa monospace -fs 10 -title 's3' -e 'sudo virsh console s3' &")

				print("Maquina S3 arrancada.")
			# Si el parametro es superior a 3 arrancaremos s4
			if(num_serv >= 4):

				# Repetimos el proceso de arranque con s4
				os.system("sudo virsh define s4.xml")
				os.system("sudo virsh start s4")
				os.system("xterm -rv -sb -rightbar -fa monospace -fs 10 -title 's4' -e 'sudo virsh console s4' &")

				print("Maquina S4 arrancada.")

			# Si el parametro es igual a 5 arrancaremos s5
			if(num_serv == 5):

				# Repetimos el proceso de arranque con s5
				os.system("sudo virsh define s5.xml")
				os.system("sudo virsh start s5")
				os.system("xterm -rv -sb -rightbar -fa monospace -fs 10 -title 's5' -e 'sudo virsh console s5' &")

				print("Maquina S5 arrancada.")

		else:
			print("ERROR - PARAMETRO INVALIDO") 

	# En caso de introducir parametro a la funcion arrancar, arrancaremos exlusivamente la maquina especificada
	if len(sys.argv) == 3:

		# Creamos los bridges a las dos redes virtuales
		os.system("sudo brctl addbr LAN1")
		os.system("sudo brctl addbr LAN2")
		os.system("sudo ifconfig LAN1 up")
		os.system("sudo ifconfig LAN2 up")

		# Arrancamos el gestor de maquinas virtuales
		os.system("HOME=/mnt/tmp sudo virt-manager")

		if(maquina == "c1"):

			print ("Arrancando c1")

			# Procedemos a arrancar c1
			os.system("sudo virsh define c1.xml")
			os.system("sudo virsh start c1")

			# Lanzamos c1 en terminales separados
			os.system("xterm -rv -sb -rightbar -fa monospace -fs 10 -title 'c1' -e 'sudo virsh console c1' &")

		if(maquina == "lb"):


			print ("Arrancando lb")
			# Procedemos a arrancar lb

			os.system("sudo virsh define lb.xml")
			os.system("sudo virsh start lb")

			# Lanzamos lb en terminales separados
			os.system("xterm -rv -sb -rightbar -fa monospace -fs 10 -title 'lb' -e 'sudo virsh console lb' &")

		if(maquina == "s1"):

			#  Proceso de arranque con s1
			os.system("sudo virsh define s1.xml")
			os.system("sudo virsh start s1")
			os.system("xterm -rv -sb -rightbar -fa monospace -fs 10 -title 's1' -e 'sudo virsh console s1' &")

			print("Maquina S1 arrancada.")

			
		if(maquina == "s2"):

			# Proceso de arranque con s2
			os.system("sudo virsh define s2.xml")
			os.system("sudo virsh start s2")
			os.system("xterm -rv -sb -rightbar -fa monospace -fs 10 -title 's2' -e 'sudo virsh console s2' &")

			print("Maquina S2 arrancada.")

			
		if(maquina == "s3"):

			# Proceso de arranque con s3
			os.system("sudo virsh define s3.xml")
			os.system("sudo virsh start s3")
			os.system("xterm -rv -sb -rightbar -fa monospace -fs 10 -title 's3' -e 'sudo virsh console s3' &")

			print("Maquina S3 arrancada.")
			
		if(maquina == "s1"):

			# Proceso de arranque con s4
			os.system("sudo virsh define s4.xml")
			os.system("sudo virsh start s4")
			os.system("xterm -rv -sb -rightbar -fa monospace -fs 10 -title 's4' -e 'sudo virsh console s4' &")

			print("Maquina S4 arrancada.")

			
		if(maquina == "s1"):

			# Proceso de arranque con s5
			os.system("sudo virsh define s5.xml")
			os.system("sudo virsh start s5")
			os.system("xterm -rv -sb -rightbar -fa monospace -fs 10 -title 's5' -e 'sudo virsh console s5' &")

			print("Maquina S5 arrancada.")

		else:
			print("ERROR - PARAMETRO INVALIDO")

###################################################################
######  funcion parar(n): para las maquinas virtuales    ##########
###################################################################

def parar(maquina):
	
	# Si no introducimos parametro pararemos todas las maquinas (numero especificado en funcion crear y guardado en fichero "num_serv.txt")
	if len(sys.argv) == 2:
		# Leemos el contenido del fichero donde tenemos guardado el numero de servidores a crear introducidos en la orden "crear" y lo guardamos en una variable
		f = open("num_serv.txt", "r")
		num_serv = int(f.read())
		f.close()


		if(num_serv >= 0):
			os.system("sudo virsh shutdown c1")
			os.system("sudo virsh shutdown lb")

			print("Parando C1 Y LB ...")

		if(num_serv >= 1):
			os.system("sudo virsh shutdown s1")

			print("Parando S1 ...")

		if(num_serv >= 2):
			os.system("sudo virsh shutdown s2")

			print("Parando S2 ...")

		if(num_serv >= 3):
			os.system("sudo virsh shutdown s3")

			print("Parando S3 ...")

		if(num_serv >= 4):
			os.system("sudo virsh shutdown s4")

			print("Parando s4 ...")

		if(num_serv >= 5):
			os.system("sudo virsh shutdown s5")

			print("Parando S5 ...")

	
			print("Paradas todas las maquinas ...")
	
	# En caso de introducir parametro a la funcion parar, pararemos exlusivamente la maquina especificada
	if len(sys.argv) == 3:
		
		# En cada caso solo paramos la maquina correspondiente
		if(maquina == "c1"):
			os.system("sudo virsh shutdown c1")

			print("Parando C1 ...")

		if(maquina == "lb"):
			os.system("sudo virsh shutdown lb")

			print("Parando LB ...")

		if(maquina == "s1"):
			os.system("sudo virsh shutdown s1")

			print("Parando S1 ...")

		if(maquina == "s2"):
			os.system("sudo virsh shutdown s2")

			print("Parando S2 ...")

		if(maquina == "s3"):
			os.system("sudo virsh shutdown s3")

			print("Parando S3 ...")

		if(maquina == "s4"):
			os.system("sudo virsh shutdown s4")

			print("Parando s4 ...")

		if(maquina == "s5"):
			os.system("sudo virsh shutdown s5")

			print("Parando S5 ...")


###################################################################################################
######  funcion destruir(n): libera el escenario, borrando todos los ficheros creados    ##########
###################################################################################################


def destruir(maquina):

	# Si no introducimos parametro destruimos todas las maquinas (numero especificado en funcion crear y guardado en fichero "num_serv.txt")
	if len(sys.argv) == 2:    
		if os.path.exists("c1.qcow2"):
			os.system("sudo virsh undefine c1")
			os.system("rm c1.qcow2 -f")

		if os.path.exists("c1.xml"):
			os.system("rm c1.xml -f")

		if os.path.exists("lb.qcow2"):
			os.system("sudo virsh undefine lb")
			os.system("rm lb.qcow2 -f")

		if os.path.exists("lb.xml"):
			os.system("rm lb.xml -f") 

		if os.path.exists("s1.qcow2"):
			os.system("sudo virsh undefine s1")
			os.system("rm s1.qcow2 -f")

		if os.path.exists("s1.xml"):
			os.system("rm s1.xml -f")

		if os.path.exists("s2.qcow2"):
			os.system("sudo virsh undefine s2")
			os.system("rm s2.qcow2 -f")

		if os.path.exists("s2.xml"):
			os.system("rm s2.xml -f")

		if os.path.exists("s3.xml"):
			os.system("rm s3.xml -f")

		if os.path.exists("s3.qcow2"):
			os.system("sudo virsh undefine s3")
			os.system("rm s3.qcow2 -f")

		if os.path.exists("s4.xml"):
			os.system("rm s4.xml -f")

		if os.path.exists("s4.qcow2"):
			os.system("sudo virsh undefine s4")
			os.system("rm s4.qcow2 -f")

		if os.path.exists("s5.xml"):
			os.system("rm s5.xml -f")

		if os.path.exists("s5.qcow2"):
			os.system("sudo virsh undefine s5")
			os.system("rm s5.qcow2 -f")

	os.system("rm -r ./mnt")
	os.system("rm ./num_serv.txt")
	os.system("rm ./cdps-vm-base-pf1.qcow2")
	os.system("cp /lab/cdps/pf1/cdps-vm-base-pf1.qcow2 /mnt/tmp/pf1")

	
	# En caso de introducir parametro a la funcion destruir, destruiremos exlusivamente la maquina especificada
	if len(sys.argv) == 3:
		
		# En cada caso solo paramos la maquina correspondiente
		if(maquina == "c1"):
			os.system("sudo virsh undefine c1")
			os.system("rm c1.qcow2 -f")
			os.system("rm c1.xml -f")

		if(maquina == "lb"):
			os.system("sudo virsh undefine lb")
			os.system("rm lb.qcow2 -f")
			os.system("rm lb.xml -f")

		if(maquina == "s1"):
			os.system("sudo virsh undefine s1")
			os.system("rm s1.qcow2 -f")
			os.system("rm s1.xml -f")

		if(maquina == "s2"):
			os.system("sudo virsh undefine s2")
			os.system("rm s2.qcow2 -f")
			os.system("rm s2.xml -f")

		if(maquina == "s3"):
			os.system("sudo virsh undefine s3")
			os.system("rm s3.qcow2 -f")
			os.system("rm s3.xml -f")

		if(maquina == "s4"):
			os.system("sudo virsh undefine s4")
			os.system("rm s4.qcow2 -f")
			os.system("rm s4.xml -f")

		if(maquina == "s5"):
			os.system("sudo virsh undefine s5")
			os.system("rm s5.qcow2 -f")
			os.system("rm s5.xml -f")

		os.system("rm -r ./mnt")

#############################################################################################
######  funcion arrancar(n): arranca las maquinas virtuales y muestra su consola   ##########
#############################################################################################


def configurar():

	# Leemos el contenido del fichero donde tenemos guardado el numero de servidores a crear introducidos en la orden "crear" y lo guardamos en una variable
	f = open("num_serv.txt", "r")
	num_serv = int(f.read())
	f.close()

	# Creamos el directorio temporal donde vamos a modificar los ficheros que tenemos que actualizar en las maquinas
	os.system("mkdir mnt")
	os.system("mkdir mnt/tmp")


	
	# Por defecto siempre habra que configurar c1 y lb
	if(num_serv >= 0):

		# Configuracion de C1

		# Creamos el fichero hostname en el que definimos el nombre de la maquina virtual c1
		os.system("touch ./mnt/tmp/hostname")
		os.system("echo c1 > ./mnt/tmp/hostname")

		# Copiamos el fichero hostname en el directorio /etc de nuestra maquina para actualizar el fichero hostname de esta
		os.system("sudo virt-copy-in -d c1 ./mnt/tmp/hostname /etc")
		# Creamos el fichero hosts 
		os.system("touch ./mnt/tmp/hosts")

		# Reescribimos por completo el fichero hosts cambiando la linea original por la adecuada para asociar la direccion 127.0.1.1 a c1
		n = open('./mnt/tmp/hosts',"w") 	    
		n.write("127.0.1.1 c1\n127.0.0.1 localhost\n::1 ip6-localhost ip6-loopback\nfe00::0 ip6-localnet\nff00::0 ip6-mcastprefix\nff02::1 ip6-allnodes\nff02::2 ip6-allrouters\nff02::3 ip6-allhosts")      		
		n.close()
		# Copiamos el fichero hosts en el directorio /etc de nuestra maquina para actualizar el fichero hosts de esta
		os.system("sudo virt-copy-in -d c1 ./mnt/tmp/hosts /etc")
		# Creamos el fichero index.html y le introducimos el contenido de la pagina html inicial de la maquina c1
		os.system("touch ./mnt/tmp/index.html")
		os.system("echo C1 > ./mnt/tmp/index.html")
	
		
		# Copiamos el fichero index.html en el directorio /var/www/html de nuestra maquina para actualizar el fichero index.html de esta
		os.system("sudo virt-copy-in -d c1 ./mnt/tmp/index.html /var/www/html")
		
		# Creamos el fichero interfaces
		os.system("touch ./mnt/tmp/interfaces")
		# Lo reescribimos para introducir las interfaces correspondientes de nuestra red para c1
		n = open('./mnt/tmp/interfaces',"w") 	    
		n.write("auto lo\niface lo inet loopback\n\nauto eth0\niface eth0 inet dhcp\n\niface eth0 inet static\naddress 10.0.1.2\nnetmask 255.255.255.0\ngateway 10.0.1.1\ndns-nameservers 10.0.1.1 ")      		
		n.close()
		# Copiamos el fichero interfaces en el directorio /etc/network de nuestra maquina para actualizar el fichero interfaces de esta
		os.system("sudo virt-copy-in -d c1 ./mnt/tmp/interfaces /etc/network")

		
		# Configuracion de lb

		# Definimos el nombre de la maquina virtual lb
		os.system("echo lb > ./mnt/tmp/hostname")

		# Copiamos el fichero hostname en el directorio /etc de nuestra maquina para actualizar el fichero hostname de esta
		os.system("sudo virt-copy-in -d lb ./mnt/tmp/hostname /etc")

		# Reescribimos por completo el fichero hosts cambiando la linea original por la adecuada para asociar la direccion 127.0.1.1 a lb
		n = open('./mnt/tmp/hosts',"w") 	    
		n.write("127.0.1.1 lb\n127.0.0.1 localhost\n::1 ip6-localhost ip6-loopback\nfe00::0 ip6-localnet\nff00::0 ip6-mcastprefix\nff02::1 ip6-allnodes\nff02::2 ip6-allrouters\nff02::3 ip6-allhosts")      		
		n.close()

		# Copiamos el fichero hosts en el directorio /etc de nuestra maquina para actualizar el fichero hosts de esta
		os.system("sudo virt-copy-in -d lb ./mnt/tmp/hosts /etc")

		# Introducimos en index.html el contenido de la pagina html inicial de la maquina lb
		os.system("echo LB > ./mnt/tmp/index.html")

		# Copiamos el fichero index.html en el directorio /var/www/html de nuestra maquina para actualizar el fichero index.html de esta
		os.system("sudo virt-copy-in -d lb ./mnt/tmp/index.html /var/www/html")

		# Reescribimos el fichero interfaces para introducir las interfaces correspondientes de nuestra red para lb
		n = open('./mnt/tmp/interfaces',"w") 	    
		n.write("auto lo\niface lo inet loopback\n\nauto eth0\niface eth0 inet dhcp\n\niface eth0 inet static\naddress 10.0.1.1\nnetmask 255.255.255.0\ngateway 10.0.1.2\ndns-nameservers 10.0.1.2\n\nauto eth1\niface eth1 inet dhcp\n\niface eth1 inet static\naddress 10.0.2.1\nnetmask 255.255.255.0\ngateway 10.0.2.0\ndns-nameservers 10.0.2.0\n ")      		
		n.close()

		# Copiamos el fichero interfaces en el directorio /etc/network de nuestra maquina para actualizar el fichero interfaces de esta
		os.system("sudo virt-copy-in -d lb ./mnt/tmp/interfaces /etc/network")

		# Edicion del fichero /etc/sysctl.conf para configurar el balanceador como router
		os.system("sudo virt-edit -a lb.qcow2 /etc/sysctl.conf -e 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/'")
	
		

	if(num_serv >= 1):

		# Configuracion de S1

		# Definimos el nombre de la maquina virtual s1
		os.system("echo s1 > ./mnt/tmp/hostname")

		# Copiamos el fichero hostname en el directorio /etc de nuestra maquina para actualizar el fichero hostname de esta
		os.system("sudo virt-copy-in -d s1 ./mnt/tmp/hostname /etc")

		# Reescribimos por completo el fichero hosts cambiando la linea original por la adecuada para asociar la direccion 127.0.1.1 a s1
		n = open('./mnt/tmp/hosts',"w") 	    
		n.write("127.0.1.1 s1\n127.0.0.1 localhost\n::1 ip6-localhost ip6-loopback\nfe00::0 ip6-localnet\nff00::0 ip6-mcastprefix\nff02::1 ip6-allnodes\nff02::2 ip6-allrouters\nff02::3 ip6-allhosts")      		
		n.close()

		# Copiamos el fichero hosts en el directorio /etc de nuestra maquina para actualizar el fichero hosts de esta
		os.system("sudo virt-copy-in -d s1 ./mnt/tmp/hosts /etc")

		# Introducimos en index.html el contenido de la pagina html inicial de la maquina s1
		os.system("echo S1 > ./mnt/tmp/index.html")
		
		# Copiamos el fichero index.html en el directorio /var/www/html de nuestra maquina para actualizar el fichero index.html de esta
		os.system("sudo virt-copy-in -d s1 ./mnt/tmp/index.html /var/www/html")

		# Reescribimos el fichero interfaces para introducir las interfaces correspondientes de nuestra red para s1
		n = open('./mnt/tmp/interfaces',"w") 	    
		n.write("auto lo\niface lo inet loopback\n\nauto eth0\niface eth0 inet dhcp\n\niface eth0 inet static\naddress 10.0.2.11\nnetmask 255.255.255.0\ngateway 10.0.2.1\ndns-nameservers 10.0.2.1\n ")      		
		n.close()

		# Copiamos el fichero interfaces en el directorio /etc/network de nuestra maquina para actualizar el fichero interfaces de esta
		os.system("sudo virt-copy-in -d s1 ./mnt/tmp/interfaces /etc/network")
	

	if(num_serv >= 2):
		# Configuracion de S2

		# Definimos el nombre de la maquina virtual s2
		os.system("echo s2 > ./mnt/tmp/hostname")

		# Copiamos el fichero hostname en el directorio /etc de nuestra maquina para actualizar el fichero hostname de esta
		os.system("sudo virt-copy-in -a s2.qcow2 ./mnt/tmp/hostname /etc")

		# Reescribimos por completo el fichero hosts cambiando la linea original por la adecuada para asociar la direccion 127.0.1.1 a s2
		n = open("./mnt/tmp/hosts","w") 	    
		n.write("127.0.1.1 s2\n127.0.0.1 localhost\n::1 ip6-localhost ip6-loopback\nfe00::0 ip6-localnet\nff00::0 ip6-mcastprefix\nff02::1 ip6-allnodes\nff02::2 ip6-allrouters\nff02::3 ip6-allhosts")      		
		n.close()

		# Copiamos el fichero hosts en el directorio /etc de nuestra maquina para actualizar el fichero hosts de esta
		os.system("sudo virt-copy-in -a s2.qcow2 ./mnt/tmp/hosts /etc")

		# Introducimos en index.html el contenido de la pagina html inicial de la maquina s1
		os.system("echo S2 > ./mnt/tmp/index.html")
		
		# Copiamos el fichero index.html en el directorio /var/www/html de nuestra maquina para actualizar el fichero index.html de esta
		os.system("sudo virt-copy-in -a s2.qcow2 ./mnt/tmp/index.html /var/www/html")

		# Reescribimos el fichero interfaces para introducir las interfaces correspondientes de nuestra red para s2
		n = open("./mnt/tmp/interfaces","w") 	    
		n.write("auto lo\niface lo inet loopback\n\nauto eth0\niface eth0 inet dhcp\n\niface eth0 inet static\naddress 10.0.2.12\nnetmask 255.255.255.0\ngateway 10.0.2.1\ndns-nameservers 10.0.2.1\n ")      		
		n.close()

		# Copiamos el fichero interfaces en el directorio /etc/network de nuestra maquina para actualizar el fichero interfaces de esta
		os.system("sudo virt-copy-in -a s2.qcow2 ./mnt/tmp/interfaces /etc/network")

	if(num_serv >= 3):

		# Configuracion de S3

		# Definimos el nombre de la maquina virtual s3
		os.system("echo s3 > ./mnt/tmp/hostname")

		# Copiamos el fichero hostname en el directorio /etc de nuestra maquina para actualizar el fichero hostname de esta
		os.system("sudo virt-copy-in -d s3 ./mnt/tmp/hostname /etc")

		# Reescribimos por completo el fichero hosts cambiando la linea original por la adecuada para asociar la direccion 127.0.1.1 a s3
		n = open('./mnt/tmp/hosts',"w") 	    
		n.write("127.0.1.1 s3\n127.0.0.1 localhost\n::1 ip6-localhost ip6-loopback\nfe00::0 ip6-localnet\nff00::0 ip6-mcastprefix\nff02::1 ip6-allnodes\nff02::2 ip6-allrouters\nff02::3 ip6-allhosts")      		
		n.close()

		# Copiamos el fichero hosts en el directorio /etc de nuestra maquina para actualizar el fichero hosts de esta
		os.system("sudo virt-copy-in -d s3 ./mnt/tmp/hosts /etc")

		# Introducimos en index.html el contenido de la pagina html inicial de la maquina s3
		os.system("echo S3 > ./mnt/tmp/index.html")
	
		# Copiamos el fichero index.html en el directorio /var/www/html de nuestra maquina para actualizar el fichero index.html de esta
		os.system("sudo virt-copy-in -d s3 ./mnt/tmp/index.html /var/www/html")

		# Reescribimos el fichero interfaces para introducir las interfaces correspondientes de nuestra red para s3
		n = open('./mnt/tmp/interfaces',"w") 	    
		n.write("auto lo\niface lo inet loopback\n\nauto eth0\niface eth0 inet dhcp\n\niface eth0 inet static\naddress 10.0.2.13\nnetmask 255.255.255.0\ngateway 10.0.2.1\ndns-nameservers 10.0.2.1\n ")      		
		n.close()

		# Copiamos el fichero interfaces en el directorio /etc/network de nuestra maquina para actualizar el fichero interfaces de esta
		os.system("sudo virt-copy-in -d s3 ./mnt/tmp/interfaces /etc/network")
	
	if(num_serv >= 4):
		# Configuracion de S4

		# Definimos el nombre de la maquina virtual s4
		os.system("echo s4 > ./mnt/tmp/hostname")

		# Copiamos el fichero hostname en el directorio /etc de nuestra maquina para actualizar el fichero hostname de esta
		os.system("sudo virt-copy-in -d s4 ./mnt/tmp/hostname /etc")

		# Reescribimos por completo el fichero hosts cambiando la linea original por la adecuada para asociar la direccion 127.0.1.1 a s4
		n = open('./mnt/tmp/hosts',"w") 	    
		n.write("127.0.1.1 s4\n127.0.0.1 localhost\n::1 ip6-localhost ip6-loopback\nfe00::0 ip6-localnet\nff00::0 ip6-mcastprefix\nff02::1 ip6-allnodes\nff02::2 ip6-allrouters\nff02::3 ip6-allhosts")      		
		n.close()

		# Copiamos el fichero hosts en el directorio /etc de nuestra maquina para actualizar el fichero hosts de esta
		os.system("sudo virt-copy-in -d s4 ./mnt/tmp/hosts /etc")

		# Introducimos en index.html el contenido de la pagina html inicial de la maquina s4
		os.system("echo S4 > ./mnt/tmp/index.html")

		# Copiamos el fichero index.html en el directorio /var/www/html de nuestra maquina para actualizar el fichero index.html de esta
		os.system("sudo virt-copy-in -d s4 ./mnt/tmp/index.html /var/www/html")

		# Reescribimos el fichero interfaces para introducir las interfaces correspondientes de nuestra red para s4
		n = open('./mnt/tmp/interfaces',"w") 	    
		n.write("auto lo\niface lo inet loopback\n\nauto eth0\niface eth0 inet dhcp\n\niface eth0 inet static\naddress 10.0.2.14\nnetmask 255.255.255.0\ngateway 10.0.2.1\ndns-nameservers 10.0.2.1\n ")      		
		n.close()

		# Copiamos el fichero interfaces en el directorio /etc/network de nuestra maquina para actualizar el fichero interfaces de esta
		os.system("sudo virt-copy-in -d s4 ./mnt/tmp/interfaces /etc/network")


	if(num_serv == 5):
		# Configuracion de S5

		# Definimos el nombre de la maquina virtual s5
		os.system("echo s5 > ./mnt/tmp/hostname")

		# Copiamos el fichero hostname en el directorio /etc de nuestra maquina para actualizar el fichero hostname de esta
		os.system("sudo virt-copy-in -d s5 ./mnt/tmp/hostname /etc")

		# Reescribimos por completo el fichero hosts cambiando la linea original por la adecuada para asociar la direccion 127.0.1.1 a s5
		n = open('./mnt/tmp/hosts',"w") 	    
		n.write("127.0.1.1 s5\n127.0.0.1 localhost\n::1 ip6-localhost ip6-loopback\nfe00::0 ip6-localnet\nff00::0 ip6-mcastprefix\nff02::1 ip6-allnodes\nff02::2 ip6-allrouters\nff02::3 ip6-allhosts")      		
		n.close()

		# Copiamos el fichero hosts en el directorio /etc de nuestra maquina para actualizar el fichero hosts de esta
		os.system("sudo virt-copy-in -d s5 ./mnt/tmp/hosts /etc")

		# Introducimos en index.html el contenido de la pagina html inicial de la maquina s5
		os.system("echo S5 > ./mnt/tmp/index.html")

		# Copiamos el fichero index.html en el directorio /var/www/html de nuestra maquina para actualizar el fichero index.html de esta
		os.system("sudo virt-copy-in -d s5 ./mnt/tmp/index.html /var/www/html")

		# Reescribimos el fichero interfaces para introducir las interfaces correspondientes de nuestra red para s5
		n = open('./mnt/tmp/interfaces',"w") 	    
		n.write("auto lo\niface lo inet loopback\n\nauto eth0\niface eth0 inet dhcp\n\niface eth0 inet static\naddress 10.0.2.15\nnetmask 255.255.255.0\ngateway 10.0.2.1\ndns-nameservers 10.0.2.1\n ")      		
		n.close()

		# Copiamos el fichero interfaces en el directorio /etc/network de nuestra maquina para actualizar el fichero interfaces de esta
		os.system("sudo virt-copy-in -d s5 ./mnt/tmp/interfaces /etc/network")

		# Una vez realizada la configuracion rearrancamos las maquinas
	os.system("python3 pf1.py arrancar")


###############################################################################################
###### Parte del programa para ejecucion de la entrada de parametros de la manera pedida ######
######                                en el enunciado                                    ######
###############################################################################################

options = {"crear": crear,
           "arrancar": arrancar,
           "parar": parar,
           "destruir": destruir,
           "configurar": configurar,
           }


if len(sys.argv) <= 1:
	sys.exit("Incorrecto uso del script, por favor introduzca parametros: pf1 <orden> <otros_parametros>")
else:
	orden = sys.argv[1]
	if len(sys.argv) == 2:
		num = 2
	if len(sys.argv) == 3:
		num = sys.argv[2]
	elif (len(sys.argv) >= 4):
		sys.exit("Incorrecto uso del script, por favor introduzca parametros: pf1 <orden> <otros_parametros>")
	
if orden in options:	
	if(orden == "configurar"):
		options[orden]()
	else:
		options[orden](num)

else:
	sys.exit("Incorrecto uso del script, por favor introduzca parametros: pf1 <orden> <otros_parametros>")
