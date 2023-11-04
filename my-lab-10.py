from netmiko import ConnectHandler

router = {
    'device_type': 'cisco_ios',
    'ip': '192.168.1.17',
    'username': 'admin',
    'password': 'admin'
}

my_ssh = ConnectHandler(**router)

user_num = input('How many user you want to create: ')
user_num = int(user_num)

while user_num >0:
    new_user=input('username: ')
    new_pass=input('password: ')
    user_cmd = 'username ' + new_user + ' privilege 15 password ' + new_pass
    config_command = [user_cmd]
    my_ssh.send_config_set(config_command)
    user_num -=1
print('============================================\n')

show_user = my_ssh.send_command('show run | inc username')
print(show_user)
print('Users created successfully')

input('Please any key to continue')
