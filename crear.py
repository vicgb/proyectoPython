#!/usr/bin/python


import sys
from subprocess import call
import os
from lxml import etree



num_serv = 2



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

outFileC = open('c1.xml', 'w')
doc.write("outFileC")

os.system("rm c1.xml")
os.system("mv outFileC c1.xml")

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

outFilel = open('lb.xml', 'w')
doc.write("outFilel")

os.system("rm lb.xml")
os.system("mv outFilel lb.xml")

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

	outFile1 = open('s1.xml', 'w')
	doc.write("outFile1")

	os.system("rm s1.xml")
	os.system("mv outFile1 s1.xml")

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
		source_disk.set("file", '/mnt/tmp/pf1/s2.qcow2')
		# Buscamos la etiqueta /devices/interfaces/source y la guardamos
		source_interface = root.find("./devices/interface/source")
		# Editamos la bridge de LAN1
		source_interface.set("bridge", 'LAN2')

		outFile2 = open('s2.xml', 'w')
		doc.write("outFile2")

		os.system("rm s2.xml")
		os.system("mv outFile2 s2.xml")

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

		outFile3 = open('s3.xml', 'w')
		doc.write("outFile3")
		os.system("rm s3.xml")
		os.system("mv outFile3 s3.xml")

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

		outFile4 = open('s4.xml', 'w')
		doc.write("outFile4")

		os.system("rm s4.xml")
		os.system("mv outFile4 s4.xml")

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

		outFile5 = open('s5.xml', 'w')
		doc.write("outFile5")

		os.system("rm s5.xml")
		os.system("mv outFile5 s5.xml")

		print("Se ha creado S5")

else:
	print("ERROR - PARAMETRO INVALIDO")	




