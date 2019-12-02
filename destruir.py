#!/usr/bin/python


import sys
from subprocess import call
import os
from lxml import etree




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
	os.system("sudo virsh undefine s3")
	os.system("rm s3.xml -f")

if os.path.exists("s3.qcow2"):
	os.system("rm s3.qcow2 -f")

if os.path.exists("s4.xml"):
	os.system("sudo virsh undefine s4")
	os.system("rm s4.xml -f")

if os.path.exists("s4.qcow2"):
	os.system("rm s4.qcow2 -f")

if os.path.exists("s5.xml"):
	os.system("sudo virsh undefine s5")
	os.system("rm s5.xml -f")

if os.path.exists("s5.qcow2"):
	os.system("rm s5.qcow2 -f")

os.system("rm -r ./mnt")
               
