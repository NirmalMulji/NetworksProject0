from socket import *
from random import randint
import sys

serverName = "paris.cs.utexas.edu"
serverPort = 35601
serverIP = gethostbyname(serverName)

# client creates a TCP socket
sock = socket(AF_INET, SOCK_STREAM)

# client opens a connection to the server's socket
try:
    sock.connect((serverName, serverPort))
except Exception:
    print "There was an error opening a connection to the server, check your server and port name"
    sys.exit(1)


clientIP, clientPort = sock.getsockname()
usernum = randint(0, 9000)
username = "N.P.MULJI"
newline = "\n"

# new socket connection
psock = socket(AF_INET, SOCK_STREAM)

newPort = clientPort + 1
psock.bind((gethostname(), newPort))
psock.listen(1)

# forming the request string
requestType = "ex1"

# address and port psock is bound to so client can see what's going on
print "psock address: " + psock.getsockname()[0]
print "psock port: ", psock.getsockname()[1]


serverEndpointSpecifier = serverIP + "-" + str(serverPort)
clientEndpointSpecifier = psock.getsockname()[0] + "-" + str(psock.getsockname()[1])

connectionSpecifier = serverEndpointSpecifier + " " + clientEndpointSpecifier

requestString = requestType + " " + connectionSpecifier + " " + str(usernum) + " " + username + newline

print requestString

# writing the client requestString to the socket
sock.send(requestString.encode())


# server confirmation
response1 = sock.recv(1024).decode()
if (response1.split()[0] != "CS"):
    print "There was an error: "
    print response1
    sys.exit(1)

response2 = sock.recv(1024).decode()
# make sure server responds with  'OK' 
if (response2.split()[0] != "OK"):
    print "Error has occured, server did not respond with 'OK'"
    print response1
    sock.close()
    sys.exit(1)

serverConfirmation = response1 + response2
print serverConfirmation

# save the random number
serverNum = int(response2.split()[3])
newsock, address = psock.accept()

#read bytes from connection socket
sentence = newsock.recv(1024).decode()
print sentence 
newservernum = int(sentence.split()[-1])
print("CS 356 server sent " + str(newservernum))
message = str(serverNum + 1) + " " + str(newservernum + 1) + " "

#send the string then close new sockets
newsock.send(message.encode())
newsock.close()
psock.close()

#receive data on the original connection then close the socket
data = sock.recv(1024).decode()
print data
sock.close()


