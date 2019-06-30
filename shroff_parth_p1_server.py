import socket
import threading
import os 
import time

def RF(name, sock):
	filename = sock.recv(1024)
	filenameconverted = filename.decode()

	str2 = filenameconverted.split()
	filenameextracted = str2[1]
	filenameextracted = filenameextracted.replace("/","")

	print(filenameextracted)
	print(filenameconverted)

	if (filenameconverted != ("GET " + "/" + filenameextracted + " HTTP/1.0\n")):
		msg1 = 'HTTP/1.0 400 Bad Request'
		convertedmsg1 = str.encode(msg1+"\n")
		sock.send(convertedmsg1)

	elif not os.path.isfile(filenameextracted):
		msg1 = 'HTTP/1.0 404 Not Found'
		convertedmsg1 = str.encode(msg1+"\n")
		sock.send(convertedmsg1)
	
	elif os.path.isfile(filenameextracted):
		msg = 'HTTP/1.0 '
		convertedmsg = str.encode(msg+"\n")
		sock.send(convertedmsg)
		
		time.sleep(1)
		
		msg1 = 'HTTP/1.1 200 OK'
		convertedmsg1 = str.encode(msg1+"\n")
		sock.send(convertedmsg1)
		
		time.sleep(1)
		
		l = "Content-Length: " + str(os.path.getsize(filenameextracted))
		sizeconvert = str.encode(l+"\n") 
		sock.send(sizeconvert)
		
		# time.sleep(1)
		
		f = open(filenameextracted, 'rb')
		bytesToSend = f.read(1024)
		sock.send(bytesToSend)
		while bytesToSend != "":
			bytesToSend = f.read(1024)
			sock.send(bytesToSend)
		
def Main():
	# Get name and port number of the host
	host = input("Enter the name of the host : ")
	port = input("Enter the port number at which host is running :")
	port = int(port)
	
	# Create socket at the host for listening
	s = socket.socket()
	s.bind((host,port))
	s.listen(5)

	print ("Server - Started.")
	
	# Keep the server running
	while True:
		c, addr = s.accept()
		# print (c)
		print (addr)
		print ("Server - Client connection is accepted")
		print ("Server - IP of the client is : " + str(addr))
		
		# Create thread to keep track of multiple connections
		t = threading.Thread(target=RF, args=("RetrThread",c))
		t.start()
	
	# Close socket when done
	s.close()

if __name__ == '__main__':
	Main()