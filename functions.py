import socket
import textwrap
import struct


# listen for packets (socket connection, infinite loop)
def main():
    connection = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3)) # connect and take care of big endian <-> little endian
    while True:
        raw_data, address = connection.recvfrom(65536)
        destination_mac, source_mac, ethernet_protocol, data = get_ethernet_frame(raw_data)
        print(f'Ethernet Frame:\n Destination: {destination_mac}, Source: {source_mac}, Protocol: {ethernet_protocol}')


# get formatted mac address
def get_mac_address(bytes_address):
    bytes_string = map('{:02x}'.format, bytes_address) # format to 2 decimal places
    return':'.join(bytes_string).upper() # returns formatted mac address
    

# unpacking ethernet frame
def get_ethernet_frame(data): # on receiving a packet
    destination_mac, source_mac, protocol = struct.unpack('! 6s 6s H', data[:14] ) # 6 bytes for source and dest, H is small unsigned int, total 14
    return get_mac_address(destination_mac), get_mac_address(source_mac), socket.htons(protocol), data[14:]




main()
