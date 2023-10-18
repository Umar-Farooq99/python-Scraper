import socket

def check_ip_port(ip_port):
    ip, port = ip_port.split(":")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((ip, int(port)))

        if result == 0:
            print(f"Success! {ip}:{port} is reachable.")
        else:
            print(f"Connection failed. {ip}:{port} is not reachable.")

        sock.close()
    except Exception as e:
        print(f"An error occurred: {e}")

# Read IP address-port combinations from a file
with open("free_proxy.txt", "r") as file:
    for line in file:
        ip_port = line.strip()
        check_ip_port(ip_port)
