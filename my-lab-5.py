from netmiko import ConnectHandler

cisco_IOL = {
    'device_type': 'cisco_ios',
    'host': '192.168.1.31',
    'username': 'admin',
    'password':'admin',
}

myssh = ConnectHandler(**cisco_IOL)

config_commands = {

    'int e0/0',
    'ip add 50.50.50.50 255.255.255.252',
    'no shut',
    'description This interface created by netmiko',
}

output = myssh.send_config_set(config_commands)
output = myssh.send_command('show ip int brief')
output = myssh.save_config()
print(output)
