from telnetlib import Telnet 

interface=input('Please enter interafce you want to configure : ')
Ipaddr=input('Please enter ip address of interface : ')
SMask=input('Please enter subnet of that ip addres : ')

connect=Telnet('192.168.1.19')
connect.write(b'admin\n')
connect.write(b'admin\n')
connect.write(b'conf t\n')

inter_cmd = 'interface ' + interface + '\n'
ipadd_cmd = 'ip address ' + Ipaddr + SMask + '\n'
 
connect.write(inter_cmd.encode('ascii'))
connect.write(ipadd_cmd.encode('ascii'))
connect.write(b' no shut \n')
connect.write(b'end\n')
connect.write(b'show ip int brief\n')
connect.write(b'exit\n')
print (connect.read_all().decode('ascii'))
input('press any key to continue')