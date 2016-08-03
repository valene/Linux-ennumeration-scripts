* os and hostname information
  ===========================

    systeminfo | findstr /B /C:"OS Name" /C:"OS Version"

    hostname 

    echo %username%

    net users

    net user username1


* network interfaces
  ==================

    ipconfig /all

    route print

    arp -A

    netstat -ano


* netsh - firewall
  ================

    netsh firewall show state

    netsh firewall show config

* process list
  =============

    tasklist /SVC

    schtasks /query /fo LIST /v

    net start

    DRIVERQUERY

* Patches
  =======

    wmic qfe get Caption,Description,HotFixID,InstalledOn

* check for pass
  ==============

    dir /s *pass* == *cred* == *vnc* == *.config*

    findstr /si password *.xml *.ini *.txt

    reg query HKLM /f password /t REG_SZ /s
   
    reg query HKCU /f password /t REG_SZ /s


* check user privileges
  =====================

    accesschk.exe -uqcqv "Authenticated Users" *


* Autologin
  =========

    reg query "HKLM\SOFTWARE\Microsoft\somedir\Currentversion\Winlogon"


* other passwords of interest
  ===========================

    reg query "HKCU\Software\ORL\Win VNC3\Password"

    reg query "HKLM\SYSTEM\Current\Control Set\Services\SNMP"

    reg query "HKCU\Software\somename\PuTTy\Sessions"


* unquoted file path
  ==================

    wmic service get name,displayname,pathname,startmode | findstr /i "Auto" |findstr /i /v "C:\Windows\\" |findstr /i /v """


* Permissions on directories
  ==========================

    icacls

    cacls


