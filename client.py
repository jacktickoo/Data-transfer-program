import socket
import sys
from fileshare import *

report = ""

def terminate(message):
	global report
	report += "Program was terminated before completion. "
	report += "Error: "
	report += message
	print(report)
	exit(1)
	
def parseFilename(command):
	name = " ".join(command)
	if name == "":
		terminate("A filename was not supplied for operation on file. ")
	else:
		return name

def main():
	global report
	report = "REPORT: "
	cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	srv_addr = (sys.argv[1], int(sys.argv[2])) 
	srv_addr_str = str(srv_addr)
	report += ("Requested connection to server at " + srv_addr_str + ". ")


	try:
		cli_sock.connect(srv_addr)
		report += ("Connection Successful. ")
	except Exception:
		terminate("Connection to server could not be established")
		

	try:
		command = sys.argv[3:]
		if command == []:
			terminate("No command given. ")
		operation = command[0]
		if operation == "put":
			filename = parseFilename(command[1:])
			try:
				cli_sock.sendall(str.encode(str(operation)+" "+filename))
			except Exception:
				terminate("Command could not be sent. ")
			report += ("Upload request on file " + filename + " sent. ")
			status = send_file(cli_sock,str(filename))
			report += ("Attempt" + filename + " sent. ")
			report += ("Process status: " + status + ". ")
		elif operation == "get":
			filename = parseFilename(command[1:])
			try:
				cli_sock.sendall(str.encode(str(operation)+" "+filename))
			except Exception:
				terminate("Command could not be sent. ")
			report += ("Download request on file " + filename + " sent. ")
			status = recv_file(cli_sock,str(filename))
			report += ("File " + filename + " received. ")
			report += ("Process status: " + status + ". ")
		elif operation == "list":
			try:
				cli_sock.sendall(str.encode(str(operation)))
			except Exception:
				terminate("Command could not be sent. ")
			report += "Directory listing request sent. "
			status = recv_list(cli_sock)
			report += ("Process status: " + status + ". ")
		else:
			terminate("No valid command given. ")
	except Exception:
		terminate("An error occured when processing the request made. ")
	finally:
		cli_sock.close()
		report += ("Connection closed.")


	print(report)
	exit(0)

main()