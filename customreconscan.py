#!/usr/bin/env python

#This is quick and dirty hacked script to do some custom scanning on target.
#The original script is of Mike Czumak, it was just hacked to fit personal choice. 
#usage : script.py ip.target. 
#dirb uses a custom list, if preferred rename it to custom path.

import sys
import subprocess
import multiprocessing
from multiprocessing import Process, Queue
import os
import time 

def multProc(targetin, scanip, port):
    jobs = []
    p = multiprocessing.Process(target=targetin, args=(scanip,port))
    jobs.append(p)
    p.start()
    return


def dnsEnum(ip_address, port):
    print "INFO: Detected DNS on " + ip_address + ":" + port
    return
    #return

def httpEnum(ip_address, port):
    print "INFO: Detected http on " + ip_address + ":" + port
    print "INFO: Performing nmap web script scan for " + ip_address + ":" + port  
    cdir = os.getcwd()  
    HTTPSCAN = "nmap -sV -Pn -vv -p %s --script=http-vhosts,http-userdir-enum,http-apache-negotiation,http-backup-finder,http-config-backup,http-default-accounts,http-methods,http-method-tamper,http-passwd,http-robots.txt -oN %s/nmap-http-%s-%s.txt %s" % (port, cdir, port, ip_address, ip_address)
    results = subprocess.check_output(HTTPSCAN, shell=True)
    HTTPVULNSCAN = "nmap -sV -Pn -vv -p %s --script=http-vuln* -oN %s/nmap-http-vuln-%s-%s.txt %s" % (port, cdir, port, ip_address, ip_address)
    subprocess.call(HTTPVULNSCAN, shell=True)
    NIKTOSCAN = "nikto -host %s -p %s >> %s/nikto-%s-%s.txt " % (ip_address, port, cdir, ip_address, port)
    subprocess.call(NIKTOSCAN, shell=True)
    DIRBUST = "dirb http://%s:%s /usr/share/wordlists/dirb/customlist.txt -S -o %s/dirb-%s.txt " %(ip_address, port, cdir, ip_address)
    subprocess.call(DIRBUST, shell=True)
    return

def httpsEnum(ip_address, port):
    print "INFO: Detected https on " + ip_address + ":" + port
    print "INFO: Performing nmap web script scan for " + ip_address + ":" + port    
    cdir = os.getcwd()
    HTTPSCANS = "nmap -sV -Pn -vv -p %s --script=http-vhosts,http-userdir-enum,http-apache-negotiation,http-backup-finder,http-config-backup,http-default-accounts,http-methods,http-method-tamper,http-passwd,http-robots.txt -oN %s/nmap-https-%s-%s.txt %s" % (port, cdir, ip_address, port, ip_address)
    results = subprocess.check_output(HTTPSCANS, shell=True)
    HTTPSVULNSCAN = "nmap -sV -Pn -vv -p %s --script=http-vuln* -oN %s/nmap-https-vuln-%s-%s.txt %s" % (port, cdir, port, ip_address, ip_address)
    subprocess.call(HTTPSVULNSCAN, shell=True)
    SSLSCAN = "nmap -sV -Pn -vv --script=ssl* -oN %s/nmap-ssl-%s.txt %s" % (cdir, ip_address, ip_address)
    subprocess.call(SSLSCAN, shell=True)
    NIKTOSCAN = "nikto -host %s -p %s >> %s/nikto-https-%s-%s.txt " % (ip_address, port, cdir, ip_address, port)
    subprocess.call(NIKTOSCAN, shell=True)
    DIRBUST = "dirb https://%s:%s /usr/share/wordlists/dirb/customlist.txt -S -o %s/dirb-%s.txt" % (ip_address, port, cdir, ip_address)
    subprocess.call(DIRBUST, shell=True)
    return

def mssqlEnum(ip_address, port):
    print "INFO: Detected MS-SQL on " + ip_address + ":" + port
    print "INFO: Performing nmap mssql script scan for " + ip_address + ":" + port    
    MSSQLSCAN = "nmap -vv -sV -Pn -p %s --script=ms-sql-info,ms-sql-config,ms-sql-dump-hashes --script-args=mssql.instance-port=1433,smsql.username-sa,mssql.password-sa -oX results/exam/nmap/%s_mssql.xml %s" % (port, ip_address, ip_address)
    results = subprocess.check_output(MSSQLSCAN, shell=True)

def sshEnum(ip_address, port):
    print "INFO: Detected SSH on " + ip_address + ":" + port
    return 

def snmpEnum(ip_address, port):
    print "INFO: Detected snmp on " + ip_address + ":" + port
    cdir = os.getcwd()
    SNMPSCAN = "nmap -vv -sV -sU -Pn -p 161,162 --script=snmp-netstat,snmp-processes %s -oN %s/nmap-snmp-%s.txt" % (ip_address, cdir, ip_address)
    subprocess.call(SNMPSCAN, shell=True)
    SNMPCHECKSCAN = "snmp-check -t %s -p %s >> %s/snmp-check-%s.txt " % (ip_address, port, cdir, ip_address)
    subprocess.call(SNMPCHECKSCAN, shell=True)
    return

def smtpEnum(ip_address, port):
    print "INFO: Detected smtp on " + ip_address + ":" + port
    cdir = os.getcwd()
    SMTPSCAN = "nmap -vv -sV -Pn -p 25,465,587 --script=smtp-vuln* %s -oN %s/nmap-smtp-%s.txt" % (ip_address , cdir, ip_address)
    subprocess.call(SMTPSCAN, shell=True)
    if port.strip() == "25":
       print "INFO : SMTP detected on port 25 (may run smtp user enum scripts)"
    else:
       print "WARNING: SMTP detected on non-standard port, smtprecon skipped (must run manually)" 
    return

def smbEnum(ip_address, port):
    print "INFO: Detected SMB on " + ip_address + ":" + port
    cdir = os.getcwd()
    SMBVULNSCAN = "nmap -vv -sV -Pn --script=smb-vuln* -oN %s/nmap-smb-vuln-%s.txt %s " % (cdir, ip_address, ip_address)
    subprocess.call(SMBVULNSCAN, shell=True)
    E4LSCAN = "enum4linux -a %s >> %s/smb-enum-%s.txt " % (ip_address, cdir, ip_address)
    subprocess.call(E4LSCAN, shell=True)
    if port.strip() == "445":
       print "INFO : SAMBA detected on port 445 (open) "
    return

def ftpEnum(ip_address, port):
    print "INFO: Detected ftp on " + ip_address + ":" + port
    cdir = os.getcwd() 
    FTPSCAN = "nmap -sV -Pn -vv -p %s --script=ftp-anon,ftp-bounce,ftp-libopie,ftp-proftpd-backdoor,ftp-vsftpd-backdoor-oN %s/nmap-ftp-%s-%s.txt %s " % (port, cdir, port, ip_address, ip_address)
    subprocess.call(FTPSCAN, shell=True)
    FTPVULNSCAN = "nmap -sV -Pn -p %s --script=ftp-vuln* -oN %s/nmap-ftp-vuln-%s-%s.txt %s" % (port, cdir, port, ip_address, ip_address)
    subprocess.call(FTPVULNSCAN, shell=True) 
    return

def nmapScan(ip_address):
   ip_address = ip_address.strip()
   print "INFO: Running general TCP/UDP nmap scans for " + ip_address
   serv_dict = {}
   cdir = os.getcwd()
   TCPSCAN = "nmap -vv -Pn -A -sC -sS -T 4 -p- -oN '%s/nmap-tcp-%s.txt' %s"  % (cdir,ip_address, ip_address)
   UDPSCAN = "nmap -vv -Pn -A -sC -sU -T 4 --top-ports 200 -oN '%s/nmap-udp-%s.txt'  %s" % (cdir,ip_address, ip_address)
   results = subprocess.check_output(TCPSCAN, shell=True)
   udpresults = subprocess.check_output(UDPSCAN, shell=True)
   lines = results.split("\n")
   for line in lines:
      ports = []
      line = line.strip()
      if ("tcp" in line) and ("open" in line) and not ("Discovered" in line):
	 while "  " in line: 
            line = line.replace("  ", " ");
         linesplit= line.split(" ")
         service = linesplit[2] # grab the service name
	 port = line.split(" ")[0] # grab the port/proto
         if service in serv_dict:
	    ports = serv_dict[service] # if the service is already in the dict, grab the port list
	 
         ports.append(port) 
	 serv_dict[service] = ports # add service to the dictionary along with the associated port(2)
   
   # go through the service dictionary to call additional targeted enumeration functions 
   for serv in serv_dict: 
      ports = serv_dict[serv]	
      if (serv == "http"):
 	 for port in ports:
	    port = port.split("/")[0]
	    multProc(httpEnum, ip_address, port)
      elif (serv == "ssl/http") or ("https" in serv):
	 for port in ports:
	    port = port.split("/")[0]
	    multProc(httpsEnum, ip_address, port)
      elif "ssh" in serv:
	 for port in ports:
	    port = port.split("/")[0]
	    multProc(sshEnum, ip_address, port)
      elif "smtp" in serv:
 	 for port in ports:
	    port = port.split("/")[0]
	    multProc(smtpEnum, ip_address, port)
      elif "snmp" in serv:
 	 for port in ports:
	    port = port.split("/")[0]
	    multProc(snmpEnum, ip_address, port)
      elif ("domain" in serv):
 	 for port in ports:
	    port = port.split("/")[0]
	    multProc(dnsEnum, ip_address, port)
      elif ("ftp" in serv):
 	 for port in ports:
	    port = port.split("/")[0]
	    multProc(ftpEnum, ip_address, port)
      elif "microsoft-ds" in serv or "netbios-ssn" in serv:	
 	 for port in ports:
	    port = port.split("/")[0]
	    multProc(smbEnum, ip_address, port)
      elif "ms-sql" in serv:
 	 for port in ports:
	    port = port.split("/")[0]
	    multProc(httpEnum, ip_address, port)
      
   print "INFO: TCP/UDP Nmap scans completed for " + ip_address 
   return

# grab the discover scan results and start scanning up hosts
print "############################################################"
print "####                      RECON SCAN                    ####"
print "####            A multi-process service scanner         ####"
print "####        http, ftp, dns, ssh, snmp, smtp, ms-sql     ####"
print "############################################################"
 
if __name__=='__main__':
    scanip = sys.argv[1]
    print "begining recon scan on " + scanip
    p = multiprocessing.Process(target=nmapScan, args=(scanip,))
    jobs = []
    jobs.append(p)
    p.start()

