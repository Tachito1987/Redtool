import socket
import os
import threading
from datetime import datetime
import re
import requests
from ipwhois import IPWhois
import whois

# Colores
verde = "\033[92m"
rojo = "\033[91m"
azul = "\033[94m"
amarillo = "\033[93m"
reset = "\033[0m"

def escanear_puertos():
    ip = input("IP objetivo (ej. 192.168.1.1): ").strip()
    try:
        socket.inet_aton(ip)
    except socket.error:
        print(f"{rojo}IP inválida{reset}")
        return

    inicio = int(input("Puerto inicial: "))
    fin = int(input("Puerto final: "))
    guardar = input("¿Guardar resultados en archivo? (s/n): ").lower()
    archivo = f"puertos_{ip.replace('.', '_')}_{datetime.now().strftime('%H%M%S')}.txt"

    print(f"{amarillo}Escaneando puertos de {ip}...{reset}\n")
    tiempo_inicio = datetime.now()

    for puerto in range(inicio, fin + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        resultado = sock.connect_ex((ip, puerto))
        if resultado == 0:
            msg = f"[✔] Puerto {puerto} ABIERTO"
            print(verde + msg + reset)
            if guardar == "s":
                with open(archivo, "a") as f:
                    f.write(msg + "\n")
        sock.close()

    duracion = (datetime.now() - tiempo_inicio).total_seconds()
    print(f"\n{azul}Escaneo finalizado en {duracion:.2f} segundos{reset}")
    if guardar == "s":
        print(f"{amarillo}Resultados guardados en {archivo}{reset}")

def escanear_red_local():
    red = input("Prefijo de red (ej. 192.168.1.): ").strip()
    guardar = input("¿Guardar resultados en archivo? (s/n): ").lower()
    archivo = f"red_{datetime.now().strftime('%H%M%S')}.txt"

    total = 254
    contador = [0]
    resultados = []
    lock = threading.Lock()

    print(f"{amarillo}Escaneando red {red}0/24...{reset}\n")

    def escanear_ip(ip):
        respuesta = os.system(f"ping -c 1 -W 1 {ip} > /dev/null 2>&1")
        with lock:
            contador[0] += 1
            progreso = f"[{contador[0]}/{total}]"

        if respuesta == 0:
            try:
                host = socket.gethostbyaddr(ip)[0]
                salida = f"{progreso} IP activa: {ip} ({host})"
            except:
                salida = f"{progreso} IP activa: {ip} (host desconocido)"
            print(verde + salida + reset)
            resultados.append(salida)
        else:
            print(f"{progreso} {rojo}No responde: {ip}{reset}")

    hilos = []
    for i in range(1, 255):
        ip = red + str(i)
        hilo = threading.Thread(target=escanear_ip, args=(ip,))
        hilos.append(hilo)
        hilo.start()

    for hilo in hilos:
        hilo.join()

    if guardar == "s":
        with open(archivo, "w") as f:
            for linea in resultados:
                f.write(linea + "\n")
        print(f"\n{amarillo}IPs activas guardadas en {archivo}{reset}")

def hacer_ping():
    ip = input("IP o dominio para hacer ping: ")
    print(f"{amarillo}Enviando ping a {ip}...{reset}\n")
    os.system(f"ping -c 4 {ip}")

def info_whois_geoip():
    objetivo = input("IP o dominio: ").strip()
    try:
        es_ip = re.match(r"^\d{1,3}(\.\d{1,3}){3}$", objetivo)

        if es_ip:
            print(f"{azul}=== WHOIS para IP ==={reset}")
            obj = IPWhois(objetivo)
            res = obj.lookup_rdap()
            print("ASN:", res.get("asn"))
            print("Org:", res.get("network", {}).get("name"))
            print("País:", res.get("network", {}).get("country"))
        else:
            print(f"{azul}=== WHOIS para dominio ==={reset}")
            w = whois.whois(objetivo)
            print("Dominio:", w.domain_name)
            print("Org:", w.get("org"))
            print("Creación:", w.get("creation_date"))
            print("Expiración:", w.get("expiration_date"))

        print(f"{azul}\n=== GEOIP (via ipinfo.io) ==={reset}")
        geo = requests.get(f"https://ipinfo.io/{objetivo}/json").json()
        for k, v in geo.items():
            print(f"{verde}{k}:{reset} {v}")

    except Exception as e:
        print(f"{rojo}Error WHOIS/GEOIP: {e}{reset}")

def dns_inverso():
    ip = input("Introduce una IP: ").strip()
    try:
        host, _, _ = socket.gethostbyaddr(ip)
        print(f"{verde}[✔] Nombre de host: {host}{reset}")
    except:
        print(f"{rojo}[✘] No se pudo resolver la IP a un nombre de host.{reset}")

def menu():
    while True:
        print(f"""{azul}
╔════════════════════════════════════════════╗
║           Herramientas de Red - Py        ║
╠════════════════════════════════════════════╣
║ 1. Escanear puertos                       ║
║ 2. Escanear red local (hosts + DNS)      ║
║ 3. Hacer ping                             ║
║ 4. Whois / GeoIP                          ║
║ 5. DNS inverso (IP → Hostname)           ║
║ 6. Salir                                  ║
╚════════════════════════════════════════════╝
{reset}""")
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            escanear_puertos()
        elif opcion == "2":
            escanear_red_local()
        elif opcion == "3":
            hacer_ping()
        elif opcion == "4":
            info_whois_geoip()
        elif opcion == "5":
            dns_inverso()
        elif opcion == "6":
            print("¡Hasta luego!")
            break
        else:
            print(rojo + "Opción inválida." + reset)

menu()






