#!/usr/bin/env python

################################################
# Sim Storage v1.1
# Creator: Vasilios Mavroudis
################################################

import base64
import serial
import time
import argparse


parser = argparse.ArgumentParser(description='**Sim Storage!**')
parser.add_argument('-pa','--path', help='Path to jpg image', required=True)
parser.add_argument('-r','--read', action='store_true', help='Read image from SIM')
parser.add_argument('-s','--store', action='store_true', help='Store image to SIM')
parser.add_argument('-po','--port', help='Serial Port', required=True)
args = vars(parser.parse_args())

serial_port = args['port']
path = args['path']
newline = "\r\n"


ser = serial.Serial(serial_port, 9600, timeout=5)

	
if (args['read']):
	print('Reading...')

	#Store on sim
	command = 'AT+CPMS="SM","SM","SM"' + newline
	ser.write(bytes(command.encode('ascii')))
	for row in ser.readlines(): print (row.decode("utf-8"))
	
	#Set Text mode
	command = 'AT+CMGF=1' + newline
	ser.write(bytes(command.encode('ascii')))
	for row in ser.readlines(): print (row.decode("utf-8"))
	
	
	#Print all messages
	command = 'AT+CMGL="ALL"' + newline
	ser.write(bytes(command.encode('ascii')))
	counter = 0
	imgData = ""
	for row in ser.readlines():
		#print (counter)
		#print (row.decode("utf-8"))
		if (counter >= 2 and counter%2==0):
			if (row.decode("utf-8") != ('OK' + newline)):
				imgData = imgData[:-2] + row.decode("utf-8")
		counter = counter + 1
	
	#print (imgData)
	
	#Decode and Store
	fh = open(path, "wb")
	fh.write(base64.b64decode(imgData))
	fh.close()
	
	print('Image was decoded and stored in ' + path)
	
elif (args['store']):
	print('Storing...')
		
	#Store on sim
	command = 'AT+CPMS="SM","SM","SM"' + newline
	ser.write(bytes(command.encode('ascii')))
	for row in ser.readlines(): print (row.decode("utf-8"))	
		
	#Delete all previous messages
	for i in range(0,40):
		command = 'AT+CMGD=' + str(i) + newline
		ser.write(bytes(command.encode('utf-8')))
		#time.sleep(1)
		for row in ser.readlines(): print (row.decode("utf-8"))
		
	command = 'AT+CPMS?' + newline
	ser.write(bytes(command.encode('utf-8')))
	for row in ser.readlines(): print (row.decode("utf-8"))
	

	#Read Image
	with open(path, "rb") as image_file:
		encoded_string = base64.b64encode(image_file.read())
	#print(encoded_string)
	
	#Slice base64
	slices = [encoded_string[i:i+159] for i in range(0, len(encoded_string), 159)]
	
	#Store on sim
	command = 'AT+CPMS="SM","SM","SM"' + newline
	ser.write(bytes(command.encode('ascii')))
	for row in ser.readlines(): print (row.decode("utf-8"))
	
	#Set Text mode
	command = 'AT+CMGF=1' + newline
	ser.write(bytes(command.encode('ascii')))
	for row in ser.readlines(): print (row.decode("utf-8"))
	
	
	#Store on sim
	for slice in slices: 
		temp = slice.decode("utf-8")
		
		command = 'AT+CMGW="0",0,"STO UNSENT"' + newline
		ser.write(bytes(command.encode('utf-8')))
		command = temp + chr(26)
		ser.write(bytes(command.encode('utf-8')))
		#time.sleep(20)
		for row in ser.readlines(): print (row.decode("utf-8"))
		
	print('Image was stored')
