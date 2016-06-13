#!/usr/bin/bash

#NOTE TO SELF:
#============
#bash function scope , 
#@main(_,variable,_) available for functions

#TO DO LIST
#==========
#1 . clean up verifyfunction
#2 . [[ ! "$1|" ]] && default file name

usage() {
  echo -e " $0 : -o filename "
  echo -e "\n \n \n"
  echo -e "Possible arguments \n"
  echo -e "\n"
  echo -e "-o \t outputfilename"
  echo -e "-h \t print usage"
  echo -e "\n"
  exit 0
}

verifunc() {
  echo "$var1"
  exit 0
}

teeprint() {
  echo -e "$@" | tee -a "$outfile"
}

info_NA() {
  echo -e "N.A. information $@" | tee -a "$outfile"
}

sectionprint() {
  echo -e "\n ############################" | tee -a "$outfile"
  echo -e "\t \t $@ \t \n"                    | tee -a "$outfile" 
  echo -e "###############################\n" | tee -a "$outfile"
}

infoprint() {
  echo -e "\n $@ : \n" | tee -a "$outfile" 
}

while getopts "o:h" optn; do
  case "${optn}" in
    o) fname=${OPTARG};;
    h) usage ;;
    *) usage ;;
  esac
done

initdata() {
  initdinfo=`ls -lhat /etc/init.d ` && teeprint "$initdinfo" || info_NA " /etc/init.d "
  initnonroot="$(find /etc/inid.d ! -uid 0 -type f | xargs ls -lhat )" && teeprint "$initnonroot" || info_NA " on non-root files in init"
  fedorainit=`ls -lhat /etc/rc.d/init.d ` && teeprint "$fedorainit" 
  fedoranonroot="$(find /etc/rc.d/init.d ! -uid 0 -type f | xargs ls -lhat )" && teeprint "$fedoranonroot " || info_NA " Not a fedora/red hat"
  rclocalinfo=`find /etc -name "rc.local" ` && teeprint "$rclocalinfo"
}

sysddata() {
  sysdinfo="$(find /etc/systemd/system/ -name *.service -o -name *.conf | xargs cat | grep -E 'ExecStart')" && teeprint "$sysdinfo" 
  sysdnonroot=`find /etc/systemd/system/ -name *.service -o -name *.conf ! -uid 0` && teeprint "NON-ROOT SERVICE : \n $sysdnonroot" || info_NA "non-root systemd services"
}

upsdata() {
  upsinfo=`ls /etc/init/` && teeprint "$upsinfo" 
  upshome1=`ls $HOME/.init/ ` && teeprint " upstart home/.init : $upshome1 "
  upshome2=`ls $XDG_CONFIG_HOME/upstart/ ` && teeprint "upstart $XDG_CONFIG_HOME : $upshome2"
  upshome3=`ls $XDG_CONFIG_DIRS` && teeprint " upstart $XDG_CONFIG_DIRS : $upshome3 "
  upshome4=`ls /usr/share/upstart/sessions ` && teeprint " /usr/share/upstart/sessions : $upshome4 "
}
  


#var1="$(uname -r)" && verifunc

[[ "$1" ]] || usage
[[ "$fname" ]] && outfile="$fname"-`date +"%d_%m_%y"`.txt && touch "$outfile"

#####Basic User info Collection########

sectionprint "BASIC USER INFO "
who1=`whoami` && teeprint $who1 || info_NA "whoami "
user_id=`id` && teeprint $user_id || info_NA "user id "
uhome0=`ls -lhat /home/` && teeprint "$uhome0" || info_NA "home directory"
uhome1=`ls -lhat /home.*/` && teeprint "$uhome1" || info_NA "home{1,2,3} directories"
rthome=`ls -lhat /root/` && teeprint "$rthome" || info_NA "Root home directory"
[[ "$rthome" ]] && rthist=` ls -lhat /root/*history ` && teeprint " $rthist " || info_NA " on root shell history"

infoprint " files with global write permissions "
wnufile="$(find / -type f -writable ! -user `whoami` ! -path "/proc/*" | xargs echo)" && teeprint "$wnufile" || info_NA "files writeable but !belonging to user"
rgufile="$(find /home/ -type f -perm -4 | xargs echo)" && teeprint "$rgufile" || info_NA "perm 4 files "
infoprint " ssh files and keys"
sshstuff=`find / -name "*id_?sa*" -o -name "known_hosts" -o -name "authorized_keys" -o -name "authorized_keys"` && teeprint "$sshstuff" || info_NA "ssh keys"

infoprint "history, sessions and startups"
hsfile=`ls -lhat ~/.*_history ` && teeprint "$hsfile" || info_NA " on shell history files"
bpfile=`ls -lhat ~/.*_profile | cut -d' ' -f1` && teeprint "bash_profile : $bpfile" || info_NA "bash_profile"
brfile=`ls -lhat ~/.bashrc | cut -d' ' -f1` && teeprint "bashrc : $brfile" || info_NA "bashrc"
xsesfile=`ls -lhat ~/.xsession | cut -d' ' -f1` && teeprint "xsessions : $xsesfile" || info_NA "xsessions "
xntfile=`ls -lhat ~/.xinitrc | cut -d' ' -f1` && teeprint "xinitrc : $xntfile" || info_NA "xinitrc"

sectionprint "BASIC CRON JOB INFO"
cronjobs=`ls -lhat /etc/cron* `&& teeprint "$cronjobs" || info_NA "cron jobs"
croncon=`cat /etc/crontab` && teeprint "$croncon" || info_NA "Contents of cron"
cronspool=`ls -lhat /var/spool/cron/crontabs` && teeprint "$cronspool" || info_NA "cron jobs in spool"
cronw=`find /etc/cron* -perm /0002 | xargs cat ` && teeprint "writable cron : \n $cronw" || info_NA "on writable crons"
anacronjobs=`ls -lhat /etc/anacrontab && cat /etc/anacrontab ` && teeprint "$anacronjobs" || info_NA "Anacron jobs"
anacronspool=`ls -lhat /var/spool/anacron` && teeprint "$anacronspool" || info_NA "on Anacron jobs in spool"


#######System Info#####################

sectionprint "SYSTEM INFO"
kernelinfo=`uname -a` && teeprint "$kernelinfo" || info_NA "on Kernel"
versinfo=`cat /proc/version ` && teeprint "$versinfo" || info_NA "on version"
rversinfo=`ls -lhat /etc/*release ` && teeprint "$rversinfo" || info_NA "on release version"
hnames="$(hostname)"."$(hostname -d)" && teeprint "$hnames" || info_NA "on host and domain name"

infoprint " SSH informations "
rootsshlogin=`grep "PermitRootLogin" /etc/ssh/sshd_config ` && teeprint "$rootsshlogin" || info_NA " on ssh root login"
hostkeyssh=`grep "HostKey" /etc/ssh/sshd_config ` && teeprint "$hostkeyssh" || info_NA " on location / presence of hostkey"
sshpw1=`cat /etc/ssh/sshd_config | grep "PasswordAuthentification" | grep -v "#" | grep "no"`
sshpw2=`cat /etc/ssh/sshd_config | grep "ChallengeResponseAuthentication" | grep -v "#" | grep "no" `
[[ "$sshpw1" ]] && [[ "$sshpw2" ]] && teeprint "password based login disabled" || teeprint "password based login Permitted: $sshpw1 , $sshpw2" 

#######Network Info#####################

sectionprint "NETWORK INFO"
ipinfo=`/sbin/ifconfig -a` || ipinfo=`ip addr` || ipinfo=`ls /sys/class/net ` && teeprint "$ipinfo" || info_NA " on network interfaces"
dnsinfo=`cat /etc/resolv.conf | grep "nameserver" ` && teeprint "$dnsinfo" || info_NA " on nameserver"
routeinfo=`route ` || routeinfo=`ip route` && teeprint "$routeinfo" || info_NA " on route"
tcp_udp=`netstat -pantu` && teeprint "$tcp_udp" || info_NA " from netstat on tcp/udp"

#########Process Informations###########

sectionprint "PROCESS INFOMATION"
prosinfo=`ps -aux` && teeprint "$prosinfo" || info_NA " on running processes"
prosls=`ps -aux | perl -lane 'print $F[10] ' | xargs -n1 ls -lhat 2>/dev/null | uniq ` && teeprint "$prosls" || info_NA " on process list"
inetdinfo=` cat /etc/inetd.conf ` && teeprint "INETD : \n $inetdinfo" || info_NA " on inetd"
inetdls=`cat /etc/inetd.conf | perl -lane ' !/#/ && print $F[6]' | xargs -n1 -I{} ls -lhat {} 2>/dev/null ` && teeprint "INETD LIST : \n $inetdls" || info_NA " on inetd services" 
xinetdinfo=` cat /etc/xinetd.conf || ls /etc/xinetd.d ` && teeprint "XINETD : \n $xinetdinfo" || info_NA " on Xinetd"
xinetdls=`cat /etc/xinetd.conf | perl -lane '!/#/ && print $F[6]' | xargs -n1 ls -lhart 2>/dev/null `
xinetdlsd=`cat /etc/xinetd.d/* | grep -E '(service|server)' ` 
[[ "$xinetdls" ]] || [[ "$xinetdlsd" ]] && teeprint "${xinedtdls:-$xinetdlsd}" || info_NA " on xinetd services"

########INIT or SYSTEMD or upstart##################

sectionprint "PROCESS ID 1"
[[ `ps -p 1 | grep 'systemd' ` ]] && sysdflag='systemd-yes' && teeprint "$sysdflag"
[[ `ps -p 1 | grep 'init' ` ]] && sysvflag='init-based-yes' && teeprint "$sysvflag"
[[ `ps -p 1 | grep 'upstart' ` ]] && upsflag='upstart-yes' && teeprint "$upsflag" 

[[ "$sysvflag" ]] && initdata
[[ "$sysdflag" ]] && sysddata
[[ "$upsflag" ]] && upsdata
usrlocalinfo=`ls -d /usr/local/etc/*/ ` && teeprint "Additonal: $usrlocalinfo" || info_NA " on additionally compiled pkgs in default location"


##########LAMP Search#################################

sectionprint "LAMP INFOMATION"
mysqlinfo=`mysql --version 2>/dev/nul` && teeprint "MYSQL : \n $mysqlinfo" || info_NA " Mysql"
[[ "$mysqlinfo" ]] && mysqlaccess1=`mysqladmin -uroot version 2>/dev/null` && teeprint "$mysqlaccess1" 
[[ "$mysqlinfo" ]] && mysqlaccess2=`mysqladmin -uroot -proot version 2>/dev/null` && teeprint "$mysqlaccess2"
pgsqlinfo=`ps -V ` && teeprint "POSTGRESQL : \n $pqsqlinfo" || info_NA  "postgressql"
[[ "$pqsqlinfo" ]] && pgsqltemp0=`psql -U psql template0 -c 'select version()' 2>/dev/null` && teeprint "$pgsqltemp0" 
[[ "$pgsqlinfo" ]] && pgsqltemp1=`psql -U psql template1 -c 'select version()' 2>/dev/null` && teeprint "$pgsqltemp1"
[[ "$pgsqlinfo" ]] && pgrestemp0=`psql -U postgres template0 -c 'select version()' 2>/dev/null` && teeprint "$pgrestemp0"
[[ "$pgsqlinfo" ]] && pgrestemp1=`psql -U postgres template1 -c 'select version()' 2>/dev/null` && teeprint "$pgrestemp1"
apacheinfo=`apache -v ; apache2 -v ; httpd -v ` && teeprint "APACHE : \n $apacheinfo" || info_NA "Apache"
apachecfg=`cat /etc/apache*/envvars | grep -v '^#' | grep -E 'APACHE_(LOG|RUN)' ` && teeprint "$apachecfg"
[[ "$apachecfg" ]] || httpfile=`find /etc/ -name "httpd.conf" ` && teeprint "$httpfile" || info_NA " httpd.conf" 
[[ "$apachecfg" ]] || apacheuser=`cat $httpfile | grep 'User'` && teeprint "$apacheuser"
[[ "$apachecfg" ]] || apachedir=` cat $httpfile | grep 'DocumentRoot' ` && teeprint "$apachedir"
[[ "$apachecfg" ]] || apacheallow=` cat $httpfile | grep 'AllowOverride' ` && teeprint "$apachecfg"
phpinfo1=`php --version || php-cgi --version || php5 --version || php5-cgi --version ` && teeprint "$phpinfo1" || info_NA " on php"
nginxinfo=`ps -aux | grep nginx` && teeprint "NGINX : \n $nginxinfo" || info_NA "on nginx"
nginxuser=`find /etc/ -name "nginx.conf" | grep 'user' ` && teeprint " $nginxuser" 


##########Executables and compilers available#################

sectionprint "COMPILERS AND EXECUTABLES - warning not 100percent accurate"
teeprint "${PATH//:/ }"
availcom=`dpkg --list | grep compil` && teeprint " $availcom" 
availcom=`rpm -qa | grep compil || yum list installed | grep compil` && teeprint " $availcom"
availcom=`pacman -Q | xargs -n -I{} bash -c ' [[ "$(pacman -Qi {} | grep compil)" ]] && echo {} ' ` && teeprint " $availcom"
teeprint " Above is not fully reliable and some most compilers fly under "

##############Mounts and Files systems######################

sectionprint "MOUNT POINTS INFORMATION"
nfsinfo=`cat /etc/exports ` && teeprint "$nfsinfo" || info_NA " NFS mounts"
fstabinfo=` cat /etc/fstab ` && teeprint "$fstabinfo " || info_NA " fstab"
fstabcred=`cat /etc/fstab | grep cred ` && teeprint " credentials : $fstabcred "


#############Mail Server Settings############################

sectionprint "MAIL SERVER SETTTINGS"
mailinfo=`ls -lhat /var/mail ` && teeprint " $mailinfo" || info_NA " Mails"
mailroot=`head /var/mail/root ` && teeprint "ROOT MAIL:  $mailroot" || info_NA " on root emails"

###################USER PRIVILEGES#############################

sectionprint "USER PRIVILEGES"
llinfo=` lastlog` && teeprint "LASTLOGIN : \n $llinfo" || info_NA " last login"
pswinfo=` cat /etc/passwd | cut -d':' -f1,2,3,4 ` && teeprint "\t /ETC/PASSWD : \n$pswinfo" || info_NA " reading passwd"
grpinfo=` cat /etc/passwd | cut -d':' -f1 | xargs -n1 id ` && teeprint " GROUPS : \n $grpinfo" || info_NA " on groups"
shadowinfo=` cat /etc/shadow ` && teeprint " IMPORTANT SHAODOW READABLE : $shadowinfo" || info_NA " shadow not readable"
sudoinfo= ` cat /etc/sudoers | grep -v '#' | grep -v -e '^$' ` && teeprint " $sudoinfo" || info_NA " sudo"
psudo1=` echo ' ' | sudo -S -1 ` && teeprint " Sudo without passwd" || info_NA " Sudo passwd"
[[ "$PATH" ]] && teeprint "${PATH//:/ }/" || info_NA " on PATH Environ"
shellinfo=` cat /etc/shells ` && teeprint " $shellinfo" || info_NA " on shells"
[[ "$umask" ]] && teeprint "$umask " || info_NA " on umask value"
login_def=` cat /etc/login.defs | grep -v '#' | grep -E 'UMASK' ` && teeprint "LOGIN.DEFS : \n $login_def" || info_NA " on login defs"
login_val=`cat /etc/login.defs | grep -v '#' | grep -E 'DAYS|AGE|METHOD' ` && teeprint " $login_val" 
infoprint " Cronjobs of users"
ucjobs=` cat /etc/passwd | cut -d':' -f1 | xargs -n1 crontab -l -u ` && teeprint " $ucjobs " || info_NA " on users cron job"
infoprint "SUID , GUID and GLOBAL writabl files"
suidfiles=` find / -perm -4000 -type f ! -path "/proc*" 2>/dev/null ` && teeprint " SUID : \n $suidfiles " || info_NA " on suid files"
wsuidfiles= ` find / -perm -4007 -type f ! -path "/proc*" 2>/dev/null ` && teeprint " Writable SUID : \n $wsuidfiles " ||  info_NA " on writable suid files"
guidfiles= ` find / -perm -2000 -type f ! -path "/proc*" 2>/dev/null ` && teeprint " GUID : \n $guidfiles " || info_NA " on guid files "
wguidfiles=` find / -perm -2007 -type f ! -path "/proc*" 2>/dev/null ` && teeprint " Writable GUID : \n $wguidfiles " || info_NA " on writable guid files"
infoprint " BACKUP FILES if any"
backupfiles= ` find / -name "*backup" -o -name "*bak" -o -name "*bkup" -o -name "*.alt" -type f ! -path "/proc*" ` && teeprint " $backupfiles" || info_NA " on backups"
infoprint "rhosts files"
rhostsfiles=` find /home -name "*.rhosts" | xargs -n1 cat ` && teeprint " $rhostsfiles"  || info_NA "On rhosts"

