import socket
import sys
from fileshare import *

report = ""

def terminate(message):
	global report
	report += "Program was terminated before completion. "
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
	
	srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create the socket on which the server will receive new connections

	try:
		srv_sock.bind(("0.0.0.0", int(sys.argv[1]))) # sys.argv[1] is the 1st argument on the command line
		srv_sock.listen(5)
	except Exception:
		terminate("Could not establish socket. ")

	# Loop forever (or at least for as long as no fatal errors occur)
	while True:
		report = "REPORT: "
		try:
			#print("Waiting for new client... ")
			cli_sock, cli_addr = srv_sock.accept()
			# Client connected!
			cli_addr_str = str(cli_addr)
			report += ("Client at "+cli_addr_str+" connected. ")
			#Parse Request
			try:
				request_raw = recv_command(cli_sock, cli_addr_str)
			except Exception:
				terminate("Error in transmission of instructions. ")
				
			request = str(request_raw).split(' ')
			
			if request[0] == "put":
				filename = parseFilename(request[1:])
				report += ("Upload requested on file "+ filename + ". ")
				status = recv_file(cli_sock, filename)
				report += ("Process status: " + status + ". ")
			elif request[0] == "get":
				filename = parseFilename(request[1:])
				report += ("Download requested on file "+ filename + ". ")
				status = send_file(cli_sock, filename)
				report += ("Process status: " + status + ". ")
			elif request[0] == "list":
				report += "Directory listing requested. "
				status = send_list(cli_sock)
				report += ("Process status: " + status + ". ")
			else:
				pass
		except Exception:
			terminate("An error occured when processing the request received. ")
		finally:
			cli_sock.close()
			report += "Connection was closed. "
		
		print(report)

	# Close the server socket as well to release its resources back to the OS
	srv_sock.close()

	# Exit with a zero value, to indicate success
	exit(0)

main()