import socket
import time
import os
def Main():
	host = '192.168.43.159'
	port = 2000
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect((host,port))
	print("Enter Client name ")
	client_name = input()
	print("Enter the password")
	password=input()
	s.send(client_name.encode('ascii'))
	s.send(password.encode('ascii'))
	auth=s.recv(1024)
	auth=auth.decode('ascii')
	#print(auth)
	if(auth=="authentication success"):
		print(auth)
	if (auth=="wrong password"):
		print(auth)
		return
	if (auth=="wrong user_name"):
		print(auth)
		return

	while(1):
		print("Enter option")
		print("1.Upload the file")
		print("2.Download the file")
		print("3.Exit")
		choice = int(input())
		s.send(str(choice).encode('ascii'))
		if(choice == 1):
			print("Enter file name ")
			file_name = input()
			flag = 0
			s.send(file_name.encode('ascii'))
			fd = open(file_name,"rb")
			l = fd.read(1024)
			while(l):
				#print(l)
				s.send(l)
				print("sent")
				l = fd.read(1024)
			#print("End of file")
			time.sleep(1)
			s.send("End of file".encode('ascii'))
		elif(choice == 2):
			print("Enter file name to download")
			file_name = input()
			s.send(file_name.encode('ascii'))
			stat = s.recv(1024)
			stat = stat.decode('ascii')
			if(stat == "-1"):
				print("File not found")
			else:
				fd = open(file_name,"wb")
				data = s.recv(1024)
				while True:
					check_string = data.decode('ascii')
					if(check_string == "End of file"):
						break
					print("Receiving")
					fd.write(data)
					data = s.recv(1024)
				fd.close()
		elif(choice == 3):
			print("Thank You For Using PES Drive")
			return
			s.close()
		else:
			print("Invalid Option.Enter a valid option")
Main()
