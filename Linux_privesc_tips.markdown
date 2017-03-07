##Introduction##

Since I have been asked by a few folks on strategies for Privilege Escalation in Linux, 
I have decided to place all some of the advices in here. 

The tips are very brief and as such for exact commands search around in relevant areas. 

This is by no means a comprehensive list and I will add up points as I remember. 

##Relevant Search Areas##

* Archwiki

* Google (naturally)

* Commandlinefu

* bashoneliners

##Strategies##

1.  Check for SUID binaries with root ownership

    sudo find / -user root -perm -4000 -print

2. Use strings on suspicious Binaries, if plaintext password was used and compiled strings might reveal them

3. If any system binary is **not called** through direct path , i.e /bin/cat , try creating an executable/script with the same binary name and export binary.

    # mkdir ~/bin/ && touch cat 
    # export PATH=~/bin:$PATH

4. If any environment variable is called directly, try exporting the environment variable with preferred comman injected. 

    # export HOME='uname -a;bash #'

5. This one is my favorite: If there is way to write, compile and give ownership to root with global executable permission, then compile a small program with suidbit. works only for compiled programs , not for interpreted scripts.

 

    
