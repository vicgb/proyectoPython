#!/usr/bin/python


import sys
from subprocess import call
import os
import subprocess
from lxml import etree


num_serv = 2



#Cogemos la ruta actual
path = os.getcwd()

print ("Arrancando máquinas por defecto (c1 y lb)")

# Creamos los bridges a las dos redes virtuales
os.system("sudo brctl addbr LAN1")
os.system("sudo brctl addbr LAN2")
os.system("sudo ifconfig LAN1 up")
os.system("sudo ifconfig LAN2 up")

# Arrancamos el gestor de maquinas virtuales
os.system("HOME=/mnt/tmp sudo virt-manager")

# Procedemos a arrancar las maquinas por defecto (c1 y lb)
os.system("sudo virsh define c1.xml")
os.system("sudo virsh start c1 ")

os.system("sudo virsh define lb.xml")
os.system("sudo virsh start lb ")

# Lanzamos c1 y lb en terminales separados
os.system("xterm -rv -sb -rightbar -fa monospace -fs 10 -title 'c1' -e 'sudo virsh console c1' &")
os.system("xterm -rv -sb -rightbar -fa monospace -fs 10 -title 'lb' -e 'sudo virsh console lb' &")

if ((num_serv >= 1) and (num_serv <= 5)):


	#  Repetimos el proceso de arranque con s1
	os.system("sudo virsh define s1.xml")
	os.system("sudo virsh start s1 ")
	os.system("xterm -rv -sb -rightbar -fa monospace -fs 10 -title 's1' -e 'sudo virsh console s1' &")

	print("Maquina S1 arrancada.")

	# Si el parametro es superior a 1 arrancaremos s2
	if(num_serv >= 2):

		# Repetimos el proceso de arranque con s3
		os.system("sudo virsh define s2.xml")
		os.system("sudo virsh start s2 ")
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



