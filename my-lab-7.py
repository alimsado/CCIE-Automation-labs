from netmiko import ConnectHandler

User_Name = input("Please enter username: ")

with open('devices.txt') as routers:
    for IP in routers:
        Router = {
            'device_type': 'cisco_ios',
            'host' : IP,
            'username' : User_Name,
            'password' : 'admin',            
        }
        my_ssh = ConnectHandler(**Router)

        config_commands = {
            'int loopback10',
            'description this loopback created by Netmiko',
        }
        output = my_ssh.send_config_set(config_commands)
        output = my_ssh.send_command('show interface description')
        print(output)
    
my_ssh.disconnect()