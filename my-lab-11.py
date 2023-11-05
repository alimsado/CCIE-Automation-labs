from netmiko import ConnectHandler




with open('devices.txt') as device:
    for IP in device:
        router = {
            'device_type': 'cisco_ios',
            'ip': IP,
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

        sh_host = my_ssh.send_command('show run | in hostname')
        hostname=sh_host.split()
        print("Users created on:  " + hostname[1])

input('Please any key to continue')
