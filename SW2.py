from netmiko import ConnectHandler
import authsw2

def configurar_SW2():
    """
    Configuración del switch SW2:
      - Cambio de hostname a SW2
      - Configuración del puerto Fa0/24 en modo trunk
      - Asignación de puertos de acceso para cada VLAN:
            Fa0/1 -> VLAN 10
            Fa0/2 -> VLAN 20
            Fa0/3 -> VLAN 30
      - Configuración de DHCP Snooping (habilitar y ajustar puertos confiables y límites)
    """
    comandos_SW2 = []
    # --- Ingreso a modo configuración ---
    comandos_SW2.append("configure terminal")
    # --- Cambio de hostname a SW2 ---
    comandos_SW2 += [
        "hostname SW2",
        "exit",
    ]
    # --- Configuración del puerto trunk para conectar con SW1 ---
    comandos_SW2 += [
        "configure terminal",
        "interface fa0/24",
        "switchport mode trunk",
        "switchport trunk allowed vlan 10,20,30",
        "ip dhcp snooping trust",  # puerto de confianza para DHCP
        "exit",
    ]
    # --- Asignación de puertos de acceso en SW2 (ejemplo) ---
    # Suponiendo que SW2 conecta servidores o dispositivos de control:
    comandos_SW2 += [
        "interface fa0/1",
        "switchport mode access",
        "switchport access vlan 10",
        "exit",
        "interface fa0/2",
        "switchport mode access",
        "switchport access vlan 20",
        "exit",
        "interface fa0/3",
        "switchport mode access",
        "switchport access vlan 30",
        "exit",
    ]
    # --- Activación de DHCP Snooping en SW2 ---
    comandos_SW2 += [
        "ip dhcp snooping",
        "ip dhcp snooping vlan 10,20,30",
        # Se configuran límites de tasa en otros puertos, si fuera necesario

        "interface fa0/1",
        "ip dhcp snooping trust",
        "exit",
        "interface fa0/2",
        "ip dhcp snooping trust",
        "exit",
        "interface fa0/3",
        "ip dhcp snooping trust",
        "exit",


        "interface range fa0/4-22",
        "ip dhcp snooping limit rate 15",
        "exit",
    ]
    comandos_SW2.append("end")
    comandos_SW2.append("write memory")
    
    print("\nConectando a SW2 y aplicando configuración...")
    try:
        net_connect = ConnectHandler(**Autenticacion.authsw2)
        net_connect.enable()
        output = net_connect.send_config_set(comandos_SW2)
        print("\n--- Resultado de la configuración en SW2 ---")
        print(output)
        
        verif = net_connect.send_command("show vlan brief")
        print("\n--- Verificación (show vlan brief) en SW2 ---")
        print(verif)
        
        net_connect.disconnect()
    except Exception as e:
        print(f"Error al configurar SW2: {e}")



    
    print("\nConectando a SW2 y aplicando configuración...")
    try:
        net_connect = ConnectHandler(**authsw2)
        net_connect.enable()

        output = net_connect.send_config_set(comandos_SW2)
        print("\n--- Resultado de la configuración en SW2 ---")
        print(output)

        # Opcional: Verificar configuración de VLANs y estado de interfaces
        verificacion = net_connect.send_command("show vlan brief")
        print("\n--- Verificación (show vlan brief) en SW2 ---")
        print(verificacion)

        net_connect.save_config()
        net_connect.disconnect()
    except Exception as e:
        print(f"Error al configurar SW2: {e}")


if __name__ == "__main__":
    # Ejecutar la configuración en SW2
    configurar_SW2()
    print("\n--- Configuración completada ---")