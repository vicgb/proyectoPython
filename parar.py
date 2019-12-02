#!/usr/bin/python


import sys
from subprocess import call
import os
from lxml import etree

num_serv = 2



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

	

