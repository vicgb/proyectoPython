

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

