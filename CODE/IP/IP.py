import socket

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    hostip=s.getsockname()[0]
    # print(hostip)
    return hostip

if __name__ == '__main__':
    print(get_ip())