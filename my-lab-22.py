from netmiko import ConnectHandler

print('\n' + '-' * 50)
print('Login Information')
print('-' * 50)
USER = input('SSH Username: ')
PASS = input('Password : ')
print('\n' + '-' * 50)

router_num = input("How many PE routers would you like to configure: ")
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

    vrf_num = input('How many VRFs would you like to configure : ')
    vrf_num = int(vrf_num)
    while vrf_num > 0:
        vrf_name = input('VRF Name: ')
        vrf_cmd = 'vrf definition ' + vrf_name
        rd_value = input('RD [ASN:NN]: ')
        rd_cmd = 'rd '+ rd_value
        rt_cmd = 'route-target both ' + rd_value
        print('RT will be set to in both directions as ' + rd_value)

        config_commands = [vrf_cmd, rd_cmd, 'address-family ipv4', rt_cmd]
        output = myssh.send_config_set(config_commands)
        print(output)
        print('RT has been be set in both directions as ' + rd_value)
        vrf_num -=1

    int_num = input('How many Interfaces would you like to configure : ')
    int_num = int(int_num)
    while int_num > 0:
        vrf_int_name = input('VRF Name: ')
        vrf_int_cmd = 'vrf forwarding ' + vrf_int_name
        int_id = input('Interface ID [Ethernet 0/0]: ')
        int_cmd = 'Interface ' + int_id
        ipaddr = input('IP Address: ')
        smask = input('Subnet Mask: ')
        ipaddr_cmd = 'IP Address  '+ ipaddr + ' ' + smask

        config_commands = [int_cmd, vrf_int_cmd, ipaddr_cmd, 'no shut']
        output = myssh.send_config_set(config_commands)
        print(output)
        int_num -=1

    as_num = input('AS#: ')
    router_bgp_cmd = 'router bgp ' + as_num
    neighbor_num = input('How many neighbors would you like to configure : ')
    neighbor_num = int(neighbor_num)

    while neighbor_num > 0:
        vrf_bgp_name = input('VRF Name: ')
        remote_ip = input('Neighbor IP: ')
        remote_as = input('remote-as: ')
        vrf_bgp_cmd = 'address-family ipv4 vrf ' + vrf_bgp_name
        remote_neighbor_cmd = 'neighbor ' + remote_ip + ' remote-as ' + remote_as

        config_commands = [router_bgp_cmd, vrf_bgp_cmd, remote_neighbor_cmd]
        output = myssh.send_config_set(config_commands)
        print(output)
        neighbor_num -= 1

    router_num -=1
input('Press ENTER to finish')
