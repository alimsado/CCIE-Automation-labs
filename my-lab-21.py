from netmiko import ConnectHandler

print('\n' + '-' * 50)
print('Login Information')
print('-' * 50)
USER = input('SSH Username: ')
PASS = input('SSH Password: ')
print('\n' + '-' * 50)

router_num = input("How many CE routers would you like to configure: ")
router_num = int(router_num)

while router_num > 0:
    hostip = input('Router IP: ')
    Router = {
        'device_type': 'cisco_ios',
        'ip': hostip,
        'username': USER,
        'password': PASS
    }

    myssh = ConnectHandler(**Router)
    hostname = myssh.send_command('show run | i host')
    x = hostname.split()
    device = x[1]


    as_num = input('AS#: ')
    router_bgp_cmd = 'router bgp ' + as_num

    network_y = input('Would you like to advertise networks [y/n]: ')
    if network_y.lower() == 'y':
        network_num = input('How many networks would you like to advertise: ')
        network_num = int(network_num)
        while network_num > 0:
            network_i = input('Network address [Ex: 199.1.1.0]: ')
            network_m = input('Subnet Mask: [255.255.255.0]: ')
            network_adv = 'network ' + network_i + ' mask ' + network_m
            config_commands = [router_bgp_cmd, network_adv]
            output = myssh.send_config_set(config_commands)
            print(output)
            network_num -= 1

    neighbor_num = input('How many neighbors would you like to configure : ')
    neighbor_num = int(neighbor_num)

    while neighbor_num > 0:
        remote_ip = input('Neighbor IP: ')
        remote_as = input('remote-as: ')
        remote_neighbor_cmd = 'neighbor ' + remote_ip + ' remote-as ' + remote_as

        config_commands = [router_bgp_cmd, remote_neighbor_cmd]
        output = myssh.send_config_set(config_commands)
        print(output)
        neighbor_num -= 1

    router_num -=1
input('Press ENTER to finish')
