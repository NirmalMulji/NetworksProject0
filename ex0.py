from socket import *
from random import randint
import sys

serverName = "paris.cs.utexas.edu"
serverPort = 35601
serverIP = gethostbyname(serverName)

# creates a TCP socket #
sock = socket(AF_INET, SOCK_STREAM)

# client opens a connection to the server's socket
try:
    sock.connect((serverName, serverPort))
except Exception:
    print "There was an error opening a connection to the server, check your server and port name"
    sys.exit(1)

# forming the request string
requestType = "ex0"
clientIP, clientPort = sock.getsockname()

serverEndpointSpecifier = serverIP + "-" + str(serverPort)
clientEndpointSpecifier = clientIP + "-" + str(clientPort)

connectionSpecifier = serverEndpointSpecifier + " " + clientEndpointSpecifier

usernum = randint(0, 9000)
username = "N.P.MULJI"
newline = "\n"
requestString = requestType + " " + connectionSpecifier + " " + str(usernum) + " " + username + newline

# writing the client requestString to the socket
sock.send(requestString.encode())

# server confirmation
response1 = sock.recv(1024).decode()

if (response1.split()[0] != "CS"):
    print "There was an error: "
    print response1
    sys.exit(1)

response2 = sock.recv(1024).decode()
serverConfirmation = response1 + response2
print serverConfirmation


if (response2.split()[0] != "OK"):
    print "Error has occured, server did not respond with 'OK'"
    print response1
    sys.exit(1)

# writing ack string to the socket
serverNum = int(response2.split()[3])
ackString = requestType + " " + str(usernum + 1) + " " + str(serverNum + 1) + newline
sock.send(ackString.encode())
print ackString

# reading data from socket
serverConfirmation2 = sock.recv(1024).decode()
if (serverConfirmation2.split()[-2] != "OK"):
    print "Error has occured reading data from the socket: "
    print serverConfirmation2
    sys.exit(1)

print serverConfirmation2

sock.close()





