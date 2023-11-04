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

        sh_host = my_ssh.send_command('show run | in hostname')
        hostname=sh_host.split()
        print("Backing up " + hostname[1])

        backupfilename = hostname[1] + '-Backup.txt'

        sh_run = my_ssh.send_command('show run')
        backupfile = open(backupfilename, "w")
        backupfile.write(sh_run)
        backupfile.close()

input('Press any key to continue')