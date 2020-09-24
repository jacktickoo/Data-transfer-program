import sys
import os
import socket

def recv_command(socket, sock_addr):
	data = bytearray(1)
	data = socket.recv(4096)
	return str(data.decode())
	
def send_file(socket, filename):
	data_to_send = b''
	try:
		with open(filename,'rb') as f:
			new_data = f.read(4096)
			while new_data != b'':
				data_to_send += new_data
				new_data = f.read(4096)
			socket.sendall(data_to_send)
		return "Success"
	except IOError:
		return "Failure: File could not be found"
	
def recv_file(socket,filename):
	if filename in os.listdir():
		return "Failure: Filename already in use"
	try:
		full_data = b''
		data = socket.recv(4096)
		while len(data) > 0:
			full_data += data
			data = socket.recv(4096)
		full_data += data
	except Exception:
		return "Failure: Data transmission error"
	
	try:
		with open(filename,'wb') as f:
			f.write(full_data)
		return "Success"
	except IOError:
		return "Failure: The recieved file could not be written to disk"

def recv_list(socket):
	files = []
	folders = []
	data = socket.recv(4096)
	try:
		raw_list = str(data.decode())
		items = raw_list.strip(']').strip('[').split(',')
		print("Files in Directory: ")
		for item in items:
			item_string = " - "+item.strip(' ').strip('\'')
			print(item_string)
		return "Success"
	except Exception:
		return "Failure: The directory listing recieved could not be parsed"
	
def send_list(socket):
	try:
		list = str(os.listdir())
	except Exception:
		return "Failure: Directory listing could not be retrieved"
	try:
		socket.sendall(str.encode(list))
	except Exception:
		return "Failure: Directory listing could not be encoded or transferred"
	return "Success"