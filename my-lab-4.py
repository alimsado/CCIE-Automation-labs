from telnetlib import Telnet 
import getpass


HOST = input('Please specify the Host IP : ')
USER = input('Please specify username : ')
PASS = getpass.getpass()

interface=input('Please enter interafce you want to configure : ')
Ipaddr=input('Please enter ip address of interface : ')
SMask=input('Please enter subnet of that ip addres : ')
description=input('Please add description for your interface')

connect=Telnet(HOST)
connect.write(USER.encode('ascii') + b'\n')
connect.write(PASS.encode('ascii') + b'\n')

connect.write(b'conf t\n')
int_cmd= 'interface ' + interface + '\n'
ipadd_cmd = 'ip address ' + Ipaddr + ' ' + SMask + '\n'
desc_cmd = description + ' ' + '\n'
 
connect.write(int_cmd.encode('ascii'))
connect.write(ipadd_cmd.encode('ascii'))
connect.write(desc_cmd.encode('ascii'))
connect.write(b' no shut \n')
connect.write(b'end\n')
connect.write(b'show ip int brief\n')
connect.write(b'exit\n')
print (connect.read_all().decode('ascii'))
input('press any key to continue')