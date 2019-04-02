import socket
import threading
import time
import os
import pandas as pd

def authentication(client_name,password):
    d={}
    #print("function1")
    df=pd.read_csv('authentication.csv')
    for i in range(len(df)):
       d[df.user_name[i]]=df.password[i]
    if(client_name in d.keys()):
    	if(d[client_name]==password):
    		#print("1")
    		c.send("authentication success".encode('ascii'))
    		return 1
    	else:
    		#print("2")
    		c.send("wrong password".encode('ascii'))
    		return 0
    else:
    	#print("3")
    	c.send("wrong user_name".encode('ascii'))
    	return 0


def handle_client(c):
	def authentication(client_name,password):
		d={}
		#print("function2")
		df=pd.read_csv('authentication.csv')
		for i in range(len(df)):
			d[df.user_name[i]]=df.password[i]
		if(client_name in d.keys()):
			if(d[client_name]==password):
				#print("1")
				c.send("authentication success".encode('ascii'))
				return 1
			else:
				#print("2")
				c.send("wrong password".encode('ascii'))
				return 0
		else:
			#print("3")
			c.send("wrong user_name".encode('ascii'))
			return 0
	client_name = c.recv(1024)
	client_name = client_name.decode('ascii')
	#print(client_name,"\n")
	password=c.recv(1024)
	password=password.decode('ascii')
	#print(password,"\n")
	auth=authentication(client_name,password)
	if auth==0:
		print("authentication failed")
		print("client disconnected")
	if auth==1:
		print("Handling Client "+client_name)
	while(1):
		choice = c.recv(1024)
		choice = choice.decode('ascii')
		if(choice == "1"):
			#print("in main while")
			file_name = c.recv(1024)
			file_name = file_name.decode('ascii')
			print("Receiving of "+file_name+" started")
			l = file_name.split(".")
			file_name = l[0] + "_server_"+client_name+"."+ l[1]
			fd = open(file_name,"wb")
			data = c.recv(1024)
			while True:
				check_string = data.decode('ascii')
				#print(check_string)
				if(check_string == "End of file"):
					print("inside check_string")
					break
				print("Receiving")
				fd.write(data)
				#print("data written")
				data = c.recv(1024)
			#print("Outside data loop")
			fd.close()
		if(choice == "2"):
			file_name = c.recv(1024)
			file_name = file_name.decode('ascii')
			only_name = file_name.split(".")
			file_list = []
			print("Requested for file :",file_name)
			path = "/Users/bhagwatisons/Desktop"
			for filename in os.listdir(path):
				file_list.append(filename)
			req_file = ""
			for i in file_list:
				if(only_name[0] in i and client_name in i):
					req_file = i
					break
			if(req_file == ""):
				c.send("-1".encode('ascii'))
			else:
				c.send("1".encode('ascii'))
				fd = open(req_file,"rb")
				l = fd.read(1024)
				while(l):
					c.send(l)
					print("Sending")
					l = fd.read(1024)
				time.sleep(1)
				c.send("End of file".encode('ascii'))
	c.close()
#####################################################
host = ""
port = 2000
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((host,port))
s.listen(5)
while(True):
	c,addr = s.accept()
	print("Accepted the client connection")
	t1 = threading.Thread(target = handle_client,args = (c,))
	t1.start()
	#t1.join()
