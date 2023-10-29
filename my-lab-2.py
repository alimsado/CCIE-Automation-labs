from telnetlib import Telnet 

connect=Telnet('192.168.1.19')
connect.write(b'admin\n')
connect.write(b'admin\n')
connect.write(b'conf t\n')
connect.write(b'interface Loopback99 \n')
connect.write(b'ip address 99.99.99.99 255.0.0.0\n')
connect.write(b'end\n')
connect.write(b'show ip int brief\n')
connect.write(b'exit\n')
print (connect.read_all().decode('ascii'))
input('press any key to continue')