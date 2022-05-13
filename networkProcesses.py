import socket
import struct
from PyQt5.QtCore import QObject, QThread, pyqtSignal
isRun = True
class Packet():
    # consider returning a packet object instead of a tuple
    pass

class NetworkProcessWorker(QThread):
    packet = pyqtSignal(object)
    finished = pyqtSignal()


    # listen for packets (socket connection, infinite loop)
    def getConnection():
        connection = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3)) # connect and take care of big endian <-> little endian
        return connection
                

    # get formatted mac address
    def get_mac_address(self,bytes_address):
        bytes_string = map('{:02x}'.format, bytes_address) # format to 2 decimal places
        return':'.join(bytes_string).upper() # returns formatted mac address

    # get formatted ip address
    def get_ip_address(self,address):
        return '.'.join(map(str, address))



    # unpacking ethernet frame
    def get_ethernet_frame(self,data): # on receiving a packet
        destination_mac, source_mac, protocol = struct.unpack('! 6s 6s H', data[:14] ) # 6 bytes for source and dest, H is small unsigned int, total 14
        return self.get_mac_address(destination_mac), self.get_mac_address(source_mac), socket.htons(protocol), data[14:]


    # unpacking ip packets
    def ipv4_packet(self,data):
        version_header_length = data[0]
        version = version_header_length >> 4 # to extract version
        header_length = (version_header_length & 15) * 4 # to extract header length
        time_to_live, protocol, source, target = struct.unpack('! 8x B B 2x 4s 4s', data[:20]) 
        return version, header_length, time_to_live, protocol, self.get_ip_address(source), self.get_ip_address(target), data[header_length:]

        # protocols

    # unpacking ICMP 
    def icmp_packet(self,data):
        icmp_type, code, checksum = struct.unpack('! B B H', data[:4])
        return icmp_type, code, checksum, data[4:]

    # unpacking tcp
    def tcp_segment(self,data):
        (source_port, destination_port, sequence, acknowledgement, offset_reserved_flags) = struct.unpack('! H H L L H', data[:14])
        offset = (offset_reserved_flags >> 12) * 4
        flag_urg = (offset_reserved_flags & 32) >> 5
        flag_ack = (offset_reserved_flags & 16) >> 5
        flag_psh = (offset_reserved_flags & 8) >> 5
        flag_rst = (offset_reserved_flags & 4) >> 5
        flag_syn = (offset_reserved_flags & 2) >> 5
        flag_fin = (offset_reserved_flags & 1)
        return source_port, destination_port, sequence, acknowledgement, flag_urg, flag_ack, flag_fin, flag_psh, flag_rst, flag_syn, data[offset:]

    # unpacking udp
    def udp_segment(self,data):
        source_port, destination_port, size, = struct.unpack('! H H 2x H', data[:8])
        return source_port, destination_port, size, data[8:]
            

    def run(self):
        # connection = getConnection()
        connection = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3)) # connect and take care of big endian <-> little endian

        while True:

            global isRun

            if not isRun:
                print('closed')
                break
            
            raw_data, address = connection.recvfrom(65535)
            destination_mac, source_mac, ethernet_protocol, data = self.get_ethernet_frame(raw_data)
            print(f'Ethernet Frame:\n Destination: {destination_mac}, Source: {source_mac}, Protocol: {ethernet_protocol}')

            if ethernet_protocol == 8:
                version, header_length, time_to_live, protocol, source, target, data = self.ipv4_packet(data)
                print('IPv4 Packet:')
                print(f'Version: {version}, Header Length: {header_length}, Time To Live: {time_to_live}, Protocol: {protocol}, Source: {source}, Target: {target} ')
                    # ICMP
                if protocol == 1:
                    icmp_type, code, checksum, data = self.icmp_packet(data)
                    print('ICMP Packet')
                    print(f'Type: {icmp_type}, Code: {code}, Checksum: {checksum}')
                    print(f'Data:\n{data}')
                    # return ("ICMP",source,target)
                    self.packet.emit(("ICMP",source,target, f"Type: {icmp_type}, Code: {code}, Checksum: {checksum}, Data: {data}"))


                    # TCP   
                if protocol == 6:
                    source_port, destination_port, sequence, acknowledgement, flag_urg, flag_ack, flag_fin, flag_psh, flag_rst, flag_syn, data = self.tcp_segment(data)
                    print("TCP Segment:")
                    print(f"Source Port: {source_port}, Destination Port: {destination_port}\nSequence: {sequence}, Acknowledgement: {acknowledgement}")
                    print(f"URG: {flag_urg}, ACK: {flag_ack}, FIN: {flag_fin}, PSH: {flag_psh}, RST: {flag_rst}, SYN: {flag_rst}, SYN: {flag_syn}")
                    print(f'Data:\n{data}')
                    # return ("TCP",source,target,source_port,destination_port)
                    self.packet.emit(("TCP",source,target,source_port,destination_port,f"{data}, Sequence: {sequence}, Acknowledgement: {acknowledgement}, URG: {flag_urg}, ACK: {flag_ack}, FIN: {flag_fin}, PSH: {flag_psh}, RST: {flag_rst}, SYN: {flag_rst}, SYN: {flag_syn}"))

                    # UDP
                elif protocol == 17:
                    source_port, destination_port, size, data = self.udp_segment(data)
                    print("UDP Segment:")
                    print(f"Source Port: {source_port}, Destination Port: {destination_port}, Length: {size}")
                    # return ("UDP",source,target,source_port,destination_port)
                    self.packet.emit(("UDP",source,target,source_port,destination_port,f"Length: {size}"))

                else:
                    print(f'Data:\n{data}')
                    # return ("unknown protocol",)
                    self.packet.emit(("Unknown Protocol",))
            else:
                print(f'Data:\n{data}')
                # return ("IPv6",)
                self.packet.emit(("IPv6",'-','-','-','-',data))
        self.quit()
        print("quit")

    # main()