# config_automatizada.py
"""
Script para automatizar la configuración de dos switches (SW1 y SW2)
utilizando Netmiko. Se configura:
  - Creación de VLANs (alumnos, docentes, admon)
  - Asignación de interfaces a cada VLAN mediante rangos
  - Apagado de puertos no utilizados
  - Configuración de puertos en modo trunk y acceso según caso
  - Configuración de DHCP Snooping y Spanning Tree
  - Comandos de verificación (show vlan, show interfaces, etc.)

Requisitos:
  - Archivo Autenticacion.py con los diccionarios:
      authsw1 para SW1 y authsw2 para SW2 (se puede extender para routers, etc.)
"""

from netmiko import ConnectHandler
import authsw1  # Se asume que este archivo define authsw1 

def configurar_SW1():
    """
    Configuración del switch SW1:
      - Configuración de VLANs: 10 (alumnos), 20 (docentes), 30 (admon)
      - Asignación de puertos a cada VLAN:
           Fa0/1-8  -> VLAN 10
           Fa0/9-16 -> VLAN 20
           Fa0/17-23 -> VLAN 30
      - Apagar puertos específicos (ejemplo: rango Fa0/2-8 y Fa0/10-16)
      - Configuración del puerto Fa0/24 como trunk (permitiendo VLANs 10,20,30)
      - Configuración de DHCP Snooping y ajuste de rate-limit en rangos de puertos
      - Configuración de Spanning Tree en modo rapid-pvst
    """


    comandos = []
    # --- Ingreso a modo configuración global ---
    comandos.append("configure terminal")
    
    # --- Creación de VLANs ---
    comandos += [
        "vlan 10",
        "name alumnos",
        "exit",
        "vlan 20",
        "name docentes",
        "exit",
        "vlan 30",
        "name admon",
        "exit",
    ]
    
    # --- Asignación de interfaces a cada VLAN ---
    # Se asignan los rangos completos para que todos queden en modo acceso
    comandos += [
        "interface range fa0/1-8",
        "switchport mode access",
        "switchport access vlan 10",
        "exit",
        "interface range fa0/9-16",
        "switchport mode access",
        "switchport access vlan 20",
        "exit",
        "interface range fa0/17-22",
        "switchport mode access",
        "switchport access vlan 30",
        "exit",
    ]
    
    # --- Configuración de port-security en el puerto activo de cada VLAN ---
    # Solo se configura port-security en el puerto designado.
    # VLAN 10: activo solo Fa0/1
    comandos += [
        "interface fa0/1",
        "switchport port-security",
        "switchport port-security maximum 1",
        "switchport port-security violation shutdown",
        "switchport port-security mac-address sticky",
        "exit",
    ]
    # VLAN 20: activo solo Fa0/9
    comandos += [
        "interface fa0/9",
        "switchport port-security",
        "switchport port-security maximum 1",
        "switchport port-security violation shutdown",
        "switchport port-security mac-address sticky",
        "exit",
    ]
    # VLAN 30: activo solo Fa0/17
    comandos += [
        "interface fa0/17",
        "switchport port-security",
        "switchport port-security maximum 1",
        "switchport port-security violation shutdown",
        "switchport port-security mac-address sticky",
        "exit",
    ]
    
    # --- Apagar (shutdown) los puertos NO utilizados en cada VLAN ---
    # En VLAN 10: se apagan Fa0/2-8
    comandos += [
        "interface range fa0/2-8",
        "shutdown",
        "exit",
    ]
    # En VLAN 20: se apagan Fa0/10-16
    comandos += [
        "interface range fa0/10-16",
        "shutdown",
        "exit",
    ]
    # En VLAN 30: se apagan Fa0/18-22
    comandos += [
        "interface range fa0/18-22",
        "shutdown",
        "exit",
    ]
    
    # --- Configuración del puerto trunk para conectar SW1 con SW2 ---
    comandos += [
        "interface fa0/24",
        "switchport mode trunk",
        "switchport trunk allowed vlan 10,20,30",
        "ip dhcp snooping trust",  # marcar como puerto de confianza
        "exit",
    ]
    
    # --- Activación de DHCP Snooping global y para las VLANs específicas ---
    comandos += [
        "ip dhcp snooping",
        "ip dhcp snooping vlan 10,20,30",
    ]
    # Se puede configurar límite de tasa en los puertos de acceso si se desea:
    comandos += [
        "interface range fa0/1,fa0/9,fa0/17",
        "ip dhcp snooping limit rate 15",
        "exit",
    ]
    
    # --- Finalizar y guardar la configuración ---
    comandos.append("end")
    comandos.append("write memory")
    
    print("\nConectando a SW1 y aplicando configuración...")
    try:
        net_connect = ConnectHandler(**authsw1)
        net_connect.enable()
        output = net_connect.send_config_set(comandos)
        print("\n--- Resultado de la configuración en SW1 ---")
        print(output)
        
        verif = net_connect.send_command("show vlan brief")
        print("\n--- Verificación (show vlan brief) en SW1 ---")
        print(verif)
        
        net_connect.disconnect()
    except Exception as e:
        print(f"Error al configurar SW1: {e}")




if __name__ == "__main__":
    # Ejecutar la configuración en SW2
    configurar_SW1()
    print("\n--- Configuración completada ---")