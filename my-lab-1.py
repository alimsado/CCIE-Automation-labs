cmd=input('Please enter your command:')
connect=Telnet('192.168.1.19')
connect.write(b'admin\n')
connect.write(b'admin\n')
connect.write(b'terminal length 0 \n')
connect.write(cmd.encode('ascii')+b'\n')
connect.write(b'exit \n')
print(connect.read_all().decode('ascii'))
input('press any key to continue')
