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
    comandos_SW1 = [
        "configure terminal",
        # --- Creación de VLANs ---
        "vlan 10",
        "name alumnos",
        "exit",
        "vlan 20",
        "name docentes",
        "exit",
        "vlan 30",
        "name admon",
        "exit",
        # --- Asignación de puertos a cada VLAN ---
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
        # --- Apagado de puertos no deseados ---
        # Se apagan puertos dentro de rangos específicos (ejemplo: Fa0/2-8 y Fa0/10-16)
        "interface range fa0/2-8,fa0/10-16",
        "shutdown",
        "exit",
        # --- Configuración del puerto trunk ---
        "interface fa0/24",
        "switchport mode trunk",
        "switchport trunk allowed vlan 10,20,30",
        "exit",
        # --- Configuración de DHCP Snooping ---
        "ip dhcp snooping",
        "ip dhcp snooping vlan 10,20,30",
        # Se configura un límite de tasa en puertos de acceso
        "interface range fa0/1-23",
        "ip dhcp snooping limit rate 15",
        "exit",
        # --- Configuración de Spanning Tree ---
        "spanning-tree mode rapid-pvst",
        "exit"
    ]
    
    print("\nConectando a SW1 y aplicando configuración...")
    try:
        net_connect = ConnectHandler(**authsw1)
        net_connect.enable()

        output = net_connect.send_config_set(comandos_SW1)
        print("\n--- Resultado de la configuración en SW1 ---")
        print(output)

        # Opcional: Verificar configuración de VLANs y puertos
        verificacion = net_connect.send_command("show vlan brief")
        print("\n--- Verificación (show vlan brief) en SW1 ---")
        print(verificacion)

        # Guardar configuración
        net_connect.save_config()
        net_connect.disconnect()
    except Exception as e:
        print(f"Error al configurar SW1: {e}")

if __name__ == "__main__":
    # Ejecutar la configuración en SW2
    configurar_SW1()