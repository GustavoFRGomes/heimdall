"""
    Auxiliary Script to validate IPv4 Addresses and MAC addresses.
"""
import re # for regular expressions
import socket

# def validateIpv4(ip):
#     result = ip.split(':')
#     if not len(result) == 4:
#         return None
#     for octet in result:
#         if int(octet) > 256:
#             octect = 256
#         if int(octet) < 0:
#             octet = 0
#     return result

def validIpv6(ipv6):
    try:
        socket.inet_pton(socket.AF_INET6, ipv6)
    except:
        return False
    return True

def validIpv4(ipv4):
    try:
        socket.inet_aton(ipv4)
    except socket.error:
        return False
    return True

def validMac(mac):
    if re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", \
            mac.lower()):
        return True
    return False
