import sys
import time
import socket
from Artemis import Decoder
import select

if len(sys.argv) < 1:
	print "ArtemisProxy"
	print "Usage:"
	print "  oscartemis.py <artemisserverip>" 
	sys.exit(1)

serverip = sys.argv[1]

ktCount = 0
selectionPacketSent = False

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(("127.0.0.1", 2011))
serversocket.listen(1)
print "Waiting for connection..."
serverSock = None

while True:
	(toClientSock, addr) = serversocket.accept()
	print "got connection from ", addr
	break


#packet header string

splitStr = "\xef\xbe\xad\xde"

print "conecting to artemis server at", serverip
toServerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



toServerSock.connect((serverip, 2010))

print "..connected"

d = Decoder()
inputs = [toServerSock, toClientSock]
outputs = []
#data from artemis server to client
buff = ""
#data from artemis client to server
fromClientBuff = ""

#list of packets extracted from stream to client
packets = []
workingPacket = ""

while(True):

	(read, write, fucked) = select.select(inputs, outputs, [])
	for r in read:
		if r is toServerSock:

			#read the data from the server
			buff = toServerSock.recv(256)
		elif r is toClientSock:
			fromClientBuff = toClientSock.recv(256)
		#scan the buffer for the start string and length
	packets = []
	startPacket = -1
	pktIndex = 0
	while pktIndex < len(buff):
		if buff[pktIndex : pktIndex + 4] == splitStr:
			pktIndex += 4
			if len(workingPacket) > 0:
				packets.append(workingPacket)
				workingPacket = ""
		else:
			workingPacket += buff[pktIndex]
			pktIndex += 1
	
	for p in packets:
		d.processPacket(p)

	if len(buff) > 0:
		toClientSock.send(buff)
		buff = ""


	if len(fromClientBuff) > 0:
		toServerSock.send(fromClientBuff)
		fromClientBuff = ""




	
		
	
	

			

			





