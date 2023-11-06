from netmiko import ConnectHandler

router_num = input("How many routers would you like to configure: ")
router_num = int(router_num)

print('\n' + '-' * 50)
print('Login Information')
print('-' * 50)
USER = input('SSH Username: ')
PASS = input('Password: ')
print('\n' + '-' * 50)

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
    router_bgp = 'router bgp ' + as_num

    neighbor_num = input('How many neighbors would you like to configure for MP-BGP : ')
    neighbor_num = int(neighbor_num)
    while neighbor_num > 0:
        remote_ip = input('Neighbor IP: ')
        remote_as = input('remote-as: ')
        remote_neighbor = 'neighbor ' + remote_ip + ' remote-as ' + remote_as
        update_source_int = input('Enter the Update Source Interface [Loopback10]: ')
        neighbor_update_source = 'Neighbor ' + remote_ip + ' update-source ' + update_source_int
        neighbor_vpnv4 = 'Neighbor ' + remote_ip + ' activate'
        config_commands = [router_bgp, remote_neighbor, neighbor_update_source,
                           'address-family vpnv4', neighbor_vpnv4]
        output = myssh.send_config_set(config_commands)
        print(output)

        route_ref = input('Would you like to specify the \' Route Reflector Option \' option for vpnv4 neighbor [y/n]: ')
        if route_ref.lower() == 'y':
            neighbor_rr = 'Neighbor ' + remote_ip + ' route-reflector-client'
            config_commands = [router_bgp, 'address-family vpnv4', neighbor_rr]
            output = myssh.send_config_set(config_commands)
            print(output)
        neighbor_num -= 1

    router_num -=1
input('Press ENTER to finish')
