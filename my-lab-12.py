from netmiko import ConnectHandler

router_num = input("How many router you want to configure: ")
router_num = int(router_num)


while router_num > 0:
    hostip = input('Router IP: ')
    USER = input('SSH username : ')
    PASS = input('SSH password : ')
    ABC = {'device_type' : 'cisco_ios' , 'ip' : hostip , 'username' : USER , 'password' : PASS }

    myssh = ConnectHandler(**ABC)
    shhost = myssh.send_command('show run | in hostname')
    hostname = shhost.split()
    print("configuring " + hostname[1])


    eigrpas = input("Please enter EIGRP as Number: ")
    routereigrp = 'router eigrp ' + eigrpas 
    network_num = input("How many network you want to enable eigrp on: ")
    network_num = int(network_num)

    while network_num > 0:
        network_itself = input (" Please specify network to enable: ")
        network_enable = 'network ' + network_itself 
        config_commands = [routereigrp, network_enable]
        output = myssh.send_config_set(config_commands)
        print(output)
        network_num -=1
    
    print('Router \"' + hostname[1] + '\" configured' )
    print('_'*80)
    router_num -=1

input("Press any key to finish")

