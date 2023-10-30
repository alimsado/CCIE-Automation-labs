from netmiko import ConnectHandler
from getpass import getpass

Host_IP = input("Please enter host ip: ")
User_Name = input("Please enter username: ")

cisco_device = {
    'device_type': 'cisco_ios',
    'host' : Host_IP,
    'username' : User_Name,
    'password' : getpass(),

}
my_ssh = ConnectHandler(**cisco_device)

config_commands = {
    'banner motd #Authorized DOSKI.LIVE users only#',
    'line console 0',
    'logging sync',
    'no exec-timeout',
}

output = my_ssh.send_config_set(config_commands)
output = my_ssh.send_command('show run | inc banner')
print(output)