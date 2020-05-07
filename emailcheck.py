#!/usr/bin/python

#Autor: Adrian Ledesma Bello
#Link: https://www.canalhacker.com

### This tool check for valid mails.

import socket as so
import pkgutil
import sys
import threading
import time

if not pkgutil.find_loader("dns.resolver"):
    print "\033[93mYou must install dns.resolver."
    print "Execute: pip install dnspython"
    exit()
else:
    import dns.resolver

try:
    domain = str(sys.argv[1])
    port = int(sys.argv[2])
    file = str(sys.argv[3])

except:
    print "\033[94mUsage: mail_checker <domain.com> <port> <file.txt>"
    print "Example: mail_checker google.com 25 emails.txt"
    exit()


file = open(file,"r+")
threads = list()
email = []
i = 0


for e in file:
	email.append(e.strip())


def checker(check_email,port,server):

    try:
	serv = so.socket(so.AF_INET, so.SOCK_STREAM)
	so.setdefaulttimeout(6)
	serv.connect((server,port))
	serv.recv(1024)
	serv.send("EHLO root\r\n")
	serv.recv(1024)
	serv.send("MAIL FROM:<hello@gmail.com>\r\n")
	serv.recv(1024)
	serv.send("RCPT TO:<" + str(check_email) + ">\r\n")
	res = serv.recv(1024)
	serv.send("QUIT\r\n")
	serv.close()

	if "250" in res: #### Maybe you should modify this.
	    print "OK: " + check_email

	else:
	    print "\033[1;31mNO OK: " + check_email + "\033[0m"
	    ff = open("No_valid.txt",'a')
	    ff.write(check_email + '\n')
	    ff.close()

    except:
	print "[*] Invalid server: " + str(server) + " : " + str(port)
	ff = open("No_valid.txt",'a')
	ff.write(check_email + '\n')
	ff.close()


while True:

    mx = dns.resolver.query(domain,'MX')

    for srv in mx:

	try:
	    server = str(srv).split(' ')[1]
	    so.setdefaulttimeout(6)
	    s = so.socket(so.AF_INET, so.SOCK_STREAM)
	    s.connect((server,port))
	    r = s.recv(1024)
	    s.send("QUIT\r\n")
	    s.close()

	except:

	    r = "aaa"

	if "220" in r: #### Meybe you must modify this.
	    print "Valid dns server: " + server

        while True:

	    if len(email) == i:
		time.sleep(3)
		print "DONE"
		exit()

	    check_email = email[i]
	    i = int(i) + 1
	    mult = threading.Thread(target=checker, args=(check_email, port, server,))
	    threads.append(mult)
	    mult.start()
	    time.sleep(0.2)

	else:
	    print "\033[33m[*] ERROR: Invalid server " + server + "\033[0m"
