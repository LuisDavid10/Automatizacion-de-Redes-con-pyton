from netmiko import ConnectHandler
import Autenticacion



net_connect = ConnectHandler(**Autenticacion)
net_connect.enable()
output = net_connect.send_command('show ip int brief')
print(output)

config_commands = ['enable', 'configure terminal','hostname SW1-py', 'int fa 0/23', 
'switchport mode access', 'switchport access vlan 100', 'exit']
output = net_connect.send_config_set(config_commands)
print(output)
output = net_connect.send_command('show ip interface brief')
print(output)