from netmiko import ConnectHandler

router_num = input("How many routers would you like to configure: ")
router_num = int(router_num)

while router_num > 0:
    hostip = input('Router IP: ')
    USER = input('SSH Username: ')
    PASS = input('Password: ')
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

    network_y = input('Would you like to advertise networks [y/n]: ')
    if network_y.lower() == 'y':
        network_num = input('How many networks would you like to advertise: ')
        network_num = int(network_num)
        while network_num > 0:
            network_i = input('Network address [Ex: 199.1.1.0]: ')
            network_m = input('Subnet Mask: [255.255.255.0]: ')
            network_adv = 'network ' + network_i + ' mask ' + network_m
            config_commands = [router_bgp,
                                network_adv]
            output = myssh.send_config_set(config_commands)
            print(output)
            network_num -= 1

    neighbor_num = input('How many neighbors would you like to configure : ')
    neighbor_num = int(neighbor_num)
    while neighbor_num > 0:
        remote_ip = input('Neighbor IP: ')
        remote_as = input('remote-as: ')
        remote_neighbor = 'neighbor ' + remote_ip + ' remote-as ' + remote_as
        config_commands = [router_bgp, remote_neighbor]
        output = myssh.send_config_set(config_commands)
        print(output)
        update_source = input('Would you like to specify the Update-Source Interface [y/n]: ')
        if update_source.lower() == 'y':
            update_source_int = input('Enter the Update Source Interface [Loopback10]: ')
            neighbor_update_source = 'Neighbor ' + remote_ip + ' update-source ' + update_source_int
            config_commands = [router_bgp, neighbor_update_source]
            output = myssh.send_config_set(config_commands)
            print(output)
        next_hop_self = input('Would you like to specify the \' Next-Hop-Self \' option [y/n]: ')
        if next_hop_self.lower() == 'y':
            neighbor_next_hop_self = 'Neighbor ' + remote_ip + ' next-hop-self'
            config_commands = [router_bgp, neighbor_next_hop_self]
            output = myssh.send_config_set(config_commands)
            print(output)
        route_ref = input('Would you like to specify the \' Route Reflector Option \' option [y/n]: ')
        if route_ref.lower() == 'y':
            neighbor_rr = 'Neighbor ' + remote_ip + ' route-reflector-client'
            config_commands = [router_bgp, neighbor_rr]
            output = myssh.send_config_set(config_commands)
            print(output)
        neighbor_num -= 1

    router_num -=1
    input('Press ENTER to finish')
