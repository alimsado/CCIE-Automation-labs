#pip install netmiko

#LAB-1: connect to device, apply and verify configurations.

from netmiko import ConnectHandler
from getpass import getpass

#Ask user for username and password
username = input ("Please enter username : ")
password = input ("Please enter password : ")
IP = input ("Please add device ip :")

#SSH into devices with entered credentials
devices = {
    "device-ip" : 'cisco_ios',
    "username" : username,
    "password": getpass(),
    'ip' : IP
}

my_ssh = ConnectHandler(** devices)

#Send command to devices

config_commands = {
    "int lo0",
    "ip int 10.10.10.10 255.255.255.255",
    "exit",
    "line console 0",
    "logging sync",
    "timeout 30"
}

output = my_ssh.send_config_set(config_commands)

#verify applied commands

output = my_ssh.send_command("show run | int lo0")
output = my_ssh.send_command("show run | sec line")



#=========================================
#LAB-2: Open file and connect to multiple devices
#=========================================

from netmiko import ConnectHandler
from getpass import getpass

#ask user for interaction
username = input ("Please enter username : ")
password = input ("Please enter password : ")

#SSH into device
try:
    with open('ciscoxe.txt') as routers:
        for IP in routers:
            xerouter = {
                'device_type': 'cisco_ios',
                'ip' : IP,
                'username' : username,
                'password' : getpass() 
            }
            my_ssh = ConnectHandler(**xerouter)

            config_commands = {
                'int lo0'
                'description this is loopback interface created by NetMiko'
            }
            output = my_ssh.send_config_set(config_commands)
            output = my_ssh.send_command('show interface description')
            print(output)
except Exception as e:
    print(f"failed to connect to {IP}: {e}")


my_ssh.disconnect()

#==================================================================================
#LAB-3: Open file and connect to multiple devices and configure multiple interfaces
#==================================================================================
# In Python, when constructing a list of commands to send to a network device using Netmiko, 
# each command in the list is treated as a separate line. 
# Netmiko handles sending each command to the device sequentially, 
# and the device itself processes each command as if it were entered on a new line. 
# You do not need to explicitly add \n to each command; Netmiko does this automatically.

from netmiko import ConnectHandler
from getpass import getpass

#ask user for interaction
username = input ("Please enter username : ")
password = input ("Please enter password : ")
interface = int(input (" How many interface you want to create on each routers : "))

try:
    with open('ciscoxe.txt') as routers:
        for IP in routers:
            xerouter = {
                'device_type': 'cisco_ios',
                'ip' : IP,
                'username' : username,
                'password' : getpass() 
            }
            my_ssh = ConnectHandler(**xerouter)

            while interface >0:
                intname = input('Please interface name ex: Gig0/0 , te0/0, lo0: ')
                intip = input('Please enter interface ip address ex 1.1.1.1 255.255.255.255')
                intstatus = input('Enable(no shut) or disable (shutdown)')
                commands = [
                     f'interface {intname}',
                     f'ip add {intip}',
                     'no shut' if intstatus == 'no shut' else 'shutdown'
                     ]
                my_ssh.send_config_set(commands)
                interface -=1

            print('===============================================\n')

            show_interface = my_ssh.send_command('show ip int brief')

            print('Interface created successfully')
except Exception as e:
            print(f"Failed to connect to {IP}: {e}")
my_ssh.disconnect()

#==================================================================================
#LAB-4: Configure Multiple routers routing protocols EIGRP
#==================================================================================
from netmiko import ConnectHandler
from getpass import getpass
import os
from netmiko import NetMikoAuthenticationException, NetmikoTimeoutException

router_num = int(input('how many router you want to configure : '))

while router_num >0:
     hostip = input("Please enter ip address of device: ")
     USER = input("SSH USERNAME :")
     PASS = input("SSH PASSWORD :")
     ROUTER = {'device_type' : 'cisco_ios','ip' : hostip, 'username' : USER, 'password': PASS }
     try:
        my_ssh = ConnectHandler(**ROUTER)

        #get router hostname :

        shhost = my_ssh.send_command('show run | in hostname')
        hostname = shhost.split()
        print("configuring " + hostname[1])

        #Configuring Router eigrp and network advertisement

        eirgpas = input('please enter eigrp as : ')
        routereigrp = 'router eigrp ' + eirgpas
        network_num = int(input('How many network you want to advertise'))

     except NetMikoAuthenticationException:
            print(f"Authentication failed for {hostip}. Please check your username and password.")
     except NetmikoTimeoutException:
            print(f"Connection timed out to {hostip}. Please check the IP address and network connectivity.")
     except Exception as e:
            print(f"An error occurred while configuring {hostip}: {str(e)}")

     while network_num > 0:
        networkeigrp = input('Please enter network address ex: 1.1.1.1 255.255.255.255 :')
        eigrpnetwork = 'network ' + networkeigrp
        commands = [routereigrp,eigrpnetwork]
        my_ssh.send_config_set(commands)
        network_num -=1
        my_ssh.disconnect()
     
     print('Router' + hostname[1] + ' \" Configured ')
     print('_'*80)
     router_num -=1

#==================================================================================
#LAB-5: Record output into file
#==================================================================================
# Common Use Cases:
# Editing Existing Files: When you want to open a file to edit its contents, "w+" allows you to both read existing data and write new data into the file.
# Clearing and Rewriting: Useful when you need to clear out old data and start fresh, such as when you're updating configuration files or logging new information.

from netmiko import ConnectHandler

router_num = input ("How many router you want to configure: ")
router_num = int(router_num)
eigrpas = input("EIGRP AS Number #: ")


while router_num > 0:
    hostip = input ("Please add the ip address of router: ")
    USER = input ("username : ")
    PASS = input ("password :")
    ABC = { 'device_type' : 'cisco_ios' , 'ip' : hostip , 'username' : USER , 'password' : PASS }
    MYSSH = ConnectHandler(**ABC)

    routereigrp = 'router eigrp ' + eigrpas
    shhost = MYSSH.send_command('show run | i hostname')
    hostname = shhost.split()
    print("configuring " + hostname[1])
    SIIB = MYSSH.send_command("show ip int brief")

    log_file = open ('TEMP.txt', "w")
    log_file.write(SIIB)
    log_file.write("\n")
    log_file.close()

    file_a = open('TEMP.txt', "r")
    lines = file_a.readlines()
    file_a.close()
    del lines[0]
    int_file = open('TEMP.txt', "w+") #open file clear content and rewrite new content
    for line in lines:
        int_file.write(line)
    int_file.close()

    with open('TEMP.txt') as FILE:
        for LINE in FILE:
            x=LINE.split()
            if (x[1] == 'IP-Address') or (x[1] == 'unassigned'):
                pass
            else:
                network_e = 'network ' + x[1] + ' 0.0.0.0'
                config_commands = [ routereigrp, network_e]
                output = MYSSH.send_config_set(config_commands)
                print(output)
    router_num -=1
    print('Router "' + hostname[1] + '" configured')
    print('_'*79)
#==================================================================================
#LAB-6: Configure Multiple routers routing protocols OSPF
#==================================================================================
from netmiko import ConnectHandler
from netmiko import NetMikoAuthenticationException,NetmikoTimeoutException
from getpass import getpass

with open('devce.txt') as routers:
     for IP in routers:
          try:
            ROUTER = {'device_type' : 'cisco_ios','ip' : IP,'username' : 'admin','password' : getpass()}
            my_ssh= ConnectHandler(**ROUTER)

            processID = input('Please OSPF PID : ')
            RID = input('Please OSPF RID : ')
            NETWORK = input('Please add Network that you want to enable OSPF on : ')
            WILDCARD = input('Please add wilcard of {NETWORK} Network that you want to enable OSPF on : ')
            AREAID = input('Please OSPF AREAID : ')
            #Enter configuration mode
            my_ssh.send_command('conf t')

            #OSPF configuration
            routerospf = 'router ospf ' + processID
            ospfRID = 'router ID ' + RID 
            ospfnetwork = 'network ' + NETWORK +' '+ WILDCARD +' '+ 'area ' + AREAID
            commands = [routerospf,ospfRID,ospfnetwork]

            output = my_ssh.send_config_set(commands)
            print(output)

            #Verification 
            verification = my_ssh.send_command('show run | sec r o')
            
          #ERROR handling Exceptions
          except (NetMikoAuthenticationException, NetmikoTimeoutException) as e:
             print(f"Failed to connect to {IP}: {e}")
          except Exception as e:
             print(f"An error occurred for {IP}: {e}")
          
          #Exit global configuration mode and disconnect
          finally:
               my_ssh.send_command('end')
               my_ssh.disconnect()

#=================================================================================
#LAB-7:Configure BGP on Multiple routers in Device.txt file
#=================================================================================
from netmiko import ConnectHandler
from netmiko import NetmikoAuthenticationException,NetmikoTimeoutException
from getpass import getpass

#ask user for interaction
USER = input ("Please enter username : ")
PASS = getpass("Please enter password : ")

with open('device.txt') as router:
     for IP in router:
          try:
               ROUTER = {'device_type' : 'cisco_ios', 'ip' : IP, 'username' : USER, 'password' : getpass() }

               my_ssh = ConnectHandler(**ROUTER)

               #USER Interaction:
               ASNUM = input('Please Enter local AS : ')
               NGHR = input('Please enter neighbor IP Address :')
               RMTAS = input('Please enter remote-as ASN: ')

               # BGP Configuration
               my_ssh.send_command('configure terminal')
               routerbgp = 'router bgp ' + ASNUM
               neighbor = 'neighbor ' + NGHR + ' ' + 'remote-as ' + RMTAS
               commands = [routerbgp, neighbor]
               output = my_ssh.send_config_set(commands)
               upsrc = input('whould you like to update Source interface of this BGP y/n : ')
               if upsrc.lower() == 'y':
                    updateint = input('Enter the update source interface ex Loopback0,Gig0/0 :')
                    neighbor_update_source = 'neighbor '+ NGHR + ' '+'update-source '+ updateint
                    commands = [routerbgp, neighbor_update_source]
                    output = my_ssh.send_config_set(commands)
                    print(output)
               nhself = input('Would you liek to configure next hop self y/n : ')
               if nhself.lower() == 'y':
                    next_hop_self = 'neighbor '+ NGHR + ' '*2+ 'next-hop-self'
                    commands = [routerbgp, next_hop_self]
                    output = my_ssh.send_config_set(commands)
                    print(output)
          #Error Handling Exceptions
          except NetMikoAuthenticationException:
                    print(f"Authentication failed for {IP}. Please check your username and password.")
          except NetmikoTimeoutException:
                    print(f"Connection timed out to {IP}. Please check the IP address and network connectivity.")
          except Exception as e:
                    print(f"An error occurred while configuring {IP}: {str(e)}")

          #Exit Global Configuration and Disconnect
          finally:
               my_ssh.send_command('end')
               my_ssh.disconnect()
#========================================================================================
#LAB-8: enable MPLS on ip addresses that enabled
#========================================================================================
from netmiko import ConnectHandler
from getpass import getpass
from netmiko import NetMikoAuthenticationException,NetMikoTimeoutException

#USERNAME AND PASSOWRD
USER = input ('Please enter username : ')
PASS = getpass ('Please Enter Password : ')
with open ('device.txt') as file:
     for IP in file:
          ROUTERS = {
               'device_type' : 'cisco_ios',
               'username' : USER,
               'password' : PASS,
               'ip' : IP
          }

          my_ssh = ConnectHandler(**ROUTERS)
          SSIB = my_ssh.send_command('show ip int brief')
          log_file = open('tempt.txt', 'w')
          log_file.write(SSIB)
          log_file.write('\n')
          log_file.close()

          file_a = open('temp.txt', 'r')
          lines = file_a.readlines()

          del lines[0]
          int_file = open('temp.txt', 'w+')

          for line in lines:
               int_file.write(line)

          int_file.close()

          with open('temp.txt') as FILE:
               for LINE in FILE:
                    x = LINE.split()
                    if (x[1] == 'ip-address') or (x[1] == 'unassigned'):
                         pass
                    elif ('thernet' in X[0]):
                         config_commands = ['interface '+ x[0], mpls ip]
                         output = my_ssh.send_config_set(config_commands)
                         print(output)
          print('-'*80)
#========================================================================================
#LAB-9: Push configs in file to cisco devices
#========================================================================================
from netmiko import ConnectHandler
from getpass import getpass
from netmiko import NetmikoAuthenticationException,NetMikoTimeoutException
x= 2
R1 = {
    'device_type': 'cisco_ios',
    'IP': '10.10.10.10',
    'username': 'admin',
    'password': 'admin',
    'secret': 'admin',
    'timeout': 30
    }
R2 = {
    'device_type': 'cisco_ios',
    'IP': '20.20.20.20',
    'username': 'admin',
    'password': 'admin',
    'secret': 'admin',
    'timeout': 30
}
try:
     while x>0:
          if x == 1:
               R1_ssh = ConnectHandler(**R1)
               R1_ssh.is_alive()
               R1_ssh.find_prompt()
               R1_ssh.enable()
               with open('R1.cfg') as config_1:
                    for line in config_1:
                         config_commands: str[line]
                         output = R1_ssh.send_config_set(config_commands)
                         print(output)
          else:
               R2_ssh = ConnectHandler(**R2)
               R1_ssh.is_alive()
               R1_ssh.find_prompt()
               R1_ssh.enable()
               with open('R2.cfg') as config_2:
                    for line in config_2:
                         config_commands: str[line]
                         output = R2_ssh.send_config_set(config_commands)
                         print(output)
     x -=1
#Error Handling Exceptions     
except NetMikoAuthenticationException:
    print(f"Auth failed to {IP}. Please double check username and password")
except NetMikoTimeoutException:
    print(f"failed to connect {IP}. Please check connection")
except Exception:
    print(f"An error occcured dute to unknown reason to {IP}") 
#Exit configuration mode and Disconnect SSH      
finally:
    my_ssh.send_command('end')
    my_ssh.disconnect()

#=========================
#Second way of LAB-9:
#=========================

from netmiko import ConnectHandler
from getpass import getpass
from netmiko import NetmikoAuthenticationException,NetMikoTimeoutException

R1 = {
    'device_type': 'cisco_ios',
    'IP': '10.10.10.10',
    'username': 'admin',
    'password': 'admin',
    'secret': 'admin',
    'timeout': 30
    }
R2 = {
    'device_type': 'cisco_ios',
    'IP': '20.20.20.20',
    'username': 'admin',
    'password': 'admin',
    'secret': 'admin',
    'timeout': 30
}
try:
    R1_ssh = ConnectHandler(**R1)
    R1_ssh.is_alive()
    R1_ssh.find_prompt()
    R1_ssh.enable()
    output = R1_ssh.send_config_from_file('R1.cfg')
    print(output)
    R2_ssh = ConnectHandler(**R2)
    R1_ssh.is_alive()
    R1_ssh.find_prompt()
    R1_ssh.enable()
    output = R1_ssh.send_config_from_file('R1.cfg')
    print(output)
#Error Handling Exceptions     
except NetMikoAuthenticationException:
    print(f"Auth failed to {IP}. Please double check username and password")
except NetMikoTimeoutException:
    print(f"failed to connect {IP}. Please check connection")
except Exception:
    print(f"An error occcured dute to unknown reason to {IP}") 
#Exit configuration mode and Disconnect SSH      
finally:
    R1_ssh.send_command('end')
    R1_ssh.send_command('end')
    R1_ssh.disconnect
    R2_ssh.disconnect

#=======================================
#LAB-10: Send Config in file to many devices
#=======================================
from netmiko import ConnectHandler
from getpass import getpass
from netmiko import NetmikoAuthenticationException,NetMikoTimeoutException

PASS = getpass('Please add password : ')
with open ('device.txt') as routers:
     for IP in routers:
          try:
               R = {'device_type': 'cisco_ios','username': 'admin','password': PASS}
               R_ssh = ConnectHandler(**R)
               output = R_ssh.send_config_from_file('config.txt')
               print(output)

          #Error Handling Exceptions     
          except NetMikoAuthenticationException:
            print(f"Auth failed to {IP}. Please double check username and password")
          except NetMikoTimeoutException:
            print(f"failed to connect {IP}. Please check connection")
          except Exception:
            print(f"An error occcured dute to unknown reason to {IP}") 
          #Exit configuration mode and Disconnect SSH      
          finally:
            R_ssh.send_command('end')
            R_ssh.disconnect
#=======================================
#LAB-11: LAB Challenge#1
#=======================================
from netmiko import ConnectHandler
from getpass import getpass
from netmiko import NetmikoAuthenticationException,NetMikoTimeoutException
import os

R1 = {
    'device_type': 'cisco_ios',
    'IP': '10.10.10.10',
    'username': 'admin',
    'password': 'admin',
    'secret': 'admin',
    'timeout': 30
    }
R2 = {
    'device_type': 'cisco_ios',
    'IP': '20.20.20.20',
    'username': 'admin',
    'password': 'admin',
    'secret': 'admin',
    'timeout': 30
}
try:
    print("Connecting to R1 --inprogress")
    R1_ssh = ConnectHandler(**R1)
    R1_ssh.is_alive()
    R1_ssh.find_prompt()
    R1_ssh.enable()
    print("Getting hostname of R1 --inprogress")
    ssh_host = R1_ssh.send_command('show run | inc hostname')
    X = ssh_host.split()
    hostname = X[1]
    backupfile = hostname + '-Backup.txt'
    print('Backing up R1 --inprogress')
    R1_ssh.send_command('terminal length 0')
    getconfig = R1_ssh.send_command('show run')
    backup = open (backupfile, "w")
    backup.write(getconfig)
    backup.close()
    print(f'{hostname} backed up successfully')
    print(output)

    print("Connecting to R1 --inprogress")
    R2_ssh = ConnectHandler(**R2)
    R2_ssh.is_alive()
    R2_ssh.find_prompt()
    R2_ssh.enable()
    print("Getting hostname of R1 --inprogress")
    R2_ssh.send_command('terminal length 0')
    ssh_host = R2_ssh.send_command('show run | inc hostname')
    X = ssh_host.split()
    hostname = X[1]
    backupfile = hostname + '-Backup.cfg'
    print('Backing up R1 --inprogress')
    getconfig = R2_ssh.send_command('show run')
    backup = open (backupfile, "w")
    backup.write(getconfig)
    backup.close()
    print(f'{hostname} backed up successfully')
    print(output)
    # with open('R1-Backup.cfg','w') as FILE:
    #      FILE.write(getconfig)
    # With statement will automatically close the file no need to close it manually.
    
#Error Handling Exceptions     
except NetMikoAuthenticationException:
    print(f"Auth failed to {IP}. Please double check username and password")
except NetMikoTimeoutException:
    print(f"failed to connect {IP}. Please check connection")
except Exception:
    print(f"An error occcured dute to unknown reason to {IP}") 
#Exit configuration mode and Disconnect SSH      
finally:
    R1_ssh.send_command('end')
    R1_ssh.send_command('end')
    R1_ssh.disconnect
    R2_ssh.disconnect

#========================================
#LAB-12: LAB Challenge#1 for many devices
#========================================
from netmiko import ConnectHandler
from netmiko import NetmikoAuthenticationException,NetMikoTimeoutException
from getpass import getpass
import os

PASS = getpass('Please add password : ')
USER = input('Please Enter username of devices: ')
SECRET = getpass('Please add secret passowrd for entering enable mode : ')

with open ("device.txt") as routers:
     for IP in routers:
          try:
               R = {'device_type' : 'cisco_ios', 'ip':IP, 'username' : USER, 'password' : PASS , 'enable_secrect': SECRET}
               R_SSH = ConnectHandler(**R)
               print(f"Connecting to {IP} .......")
               R_SSH.is_alive()
               R_SSH.enable()
               R_SSH.find_prompt()
               R_SSH.session_log('log.txt')

               print(f'Getting hostname of {IP}.......')
               get_hostname = R_SSH.send_command('show run | inc hostname')
               X = get_hostname.split()
               hostname = X[1]
               
               
               print(f'Creating frile for router {IP} ........')
               FILE = hostname + '-Backup.cfg'
               
               
               print(f'Getting running config of {IP} ........')

               get_runconfig = R_SSH.send_command('show running-config')
               R_SSH.send_command('terminal length 0')
               print('backing up device {IP}..........')
               with open(FILE, 'w') as BACKUP:
                   BACKUP.write(get_runconfig)
          
          #Error Handling Exceptions 

          except NetMikoAuthenticationException:
               print(f'Authentication failed for {IP}. Please check username and password')
          except NetMikoTimeoutException:
               print(f'Failed to connect {IP}. Please Connectivity ...... ')
          except Exception:
               print(f'An error occured while connnecting to {IP}. Please check device and your connectivity ')
          finally:
               R_SSH.disconnect()
#=======================================
#LAB-13: LAB Challenge#2
#=======================================
from netmiko import ConnectHandler
from netmiko import NetmikoAuthenticationException,NetmikoTimeoutException
from getpass import getpass
import os

R1 = {"device_type":'cisco_ios','username':'admin', 'password' : 'admin', 'ip' : '10.100.10.1'}
R2 = {"device_type":'cisco_ios','username':'admin', 'password' : 'admin', 'ip' : '10.100.10.2'}
ASA = {"device_type":'cisco_asa','username':'admin', 'password' : 'admin', 'ip' : '10.100.10.3'}

device = [R1,R2,ASA]

try:
    def device_config(dev):
        for dev in device:
            print(f"Connecting to {dev}.................")
            my_ssh = ConnectHandler(**dev)
            my_ssh.enable()
            my_ssh.session_log('log.txt')
            print(f"getting hostname of {dev} .......")
            hostname = my_ssh.send_command('show run | in hostname').split()[1]
            if "fw" in hostname:
                my_ssh.send_command("terminal pager 0")
            else:
                my_ssh.send_command("terminal length 0")

            print(f"Getting show running-config {dev}......")
            get_config = my_ssh.send_command('show running-config')

            print(f'backing up {dev} .......')
            with open(hostname + '-backup.cfg', 'w') as backup:
                backup.write(get_config)
            print(f"{dev} backed up successfully :)))))")

    for item in device:
        device_config(item)

#Error Handling Exceptions 

except NetMikoAuthenticationException:
    print(f'Authentication failed for {IP}. Please check username and password')
except NetMikoTimeoutException:
    print(f'Failed to connect {IP}. Please Connectivity ...... ')
except Exception:
    print(f'An error occured while connnecting to {IP}. Please check device and your connectivity ')
finally:
    my_ssh.disconnect()         

#=======================================
#LAB-14: 
#=======================================



          
          



































































#========================================
#LAB-4: Backup cisco devices
#========================================

from netmiko import ConnectHandler
from getpass import getpass

#Ask user for input
username = input ("Please add username :")
password = input ("Please add password :")

#SSH into device

cisco = {
    "username" : username,
    "password" : getpass(),
    "hostip" : hostip
}

my_ssh = ConnectHandler(**cisco)

gethost = my_ssh.send_command("show run | in hostname")
hostname = gethost.split()
print("backing up"+hostname[1])
backupfile = hostname[1] + '-backup.txt'

getconfig = my_ssh.send_command('show running-config')
backup = open (backupfile, "w")
backupfile.write(getconfig)
backupfile.close()

print(hostname[1] + 'Backed up successfully')
my_ssh.disconnect()

#====================================
#LAB-5:
#====================================
