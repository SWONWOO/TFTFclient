# -*- coding: utf-8 -*-
from __future__ import print_function
import socket
import struct
import sys

class TFTPClient:
    def __init__(self, server_ip, server_port=69):
        # 초기화 메서드: TFTP 클라이언트 객체를 생성하고 서버 주소 및 소켓 설정
        self.server_address = (server_ip, server_port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.settimeout(5)

    def send_rrq(self, filename):
        # RRQ(Read Request) 패킷 전송 메소드
        rrq_packet = struct.pack("!H", 1) + filename.encode() + b'\0octet\0'
        self.client_socket.sendto(rrq_packet, self.server_address)

    def send_wrq(self, filename):
        # WRQ(Write Request) 패킷 전송 메소드
        wrq_packet = struct.pack("!H", 2) + filename.encode() + b'\0octet\0'
        self.client_socket.sendto(wrq_packet, self.server_address)

    def receive_data(self):
        # 데이터 수신 및 처리 메소드
        try:
            data, address = self.client_socket.recvfrom(516)
            opcode, block_number = struct.unpack("!HH", data[:4])

            if opcode == 3:
                return block_number, data[4:]
            elif opcode == 5:
                error_code = struct.unpack("!H", data[4:6])[0]
                error_msg = data[6:].decode()
                print("Error {}: {}".format(error_code, error_msg))
                sys.exit(1)
        except socket.timeout:
            print("Timeout")
            sys.exit(1)

    def download_file(self, filename):
        # 파일 다운로드 메소드
        self.send_rrq(filename)
        block_number = 1

        with open(filename, 'wb') as file:
            while True:
                data_block = self.receive_data()
                if data_block[0] == block_number:
                    file.write(data_block[1])
                    ack_packet = struct.pack("!HH", 4, block_number)
                    self.client_socket.sendto(ack_packet, self.server_address)
                    block_number += 1
                else:
                    print("Received out-of-order data block. Ignoring.")

    def upload_file(self, filename):
        # 파일 업로드 메소드
        self.send_wrq(filename)
        block_number = 1

        with open(filename, 'rb') as file:
            data = file.read(512)
            while data:
                data_packet = struct.pack("!HH", 3, block_number) + data
                self.client_socket.sendto(data_packet, self.server_address)

                ack_received = False
                while not ack_received:
                    try:
                        ack_data, _ = self.client_socket.recvfrom(4)
                        ack_opcode, ack_block_number = struct.unpack("!HH", ack_data)
                        if ack_opcode == 4 and ack_block_number == block_number:
                            ack_received = True
                    except socket.timeout:
                        print("Timeout waiting for ACK. Resending data block.")
                        self.client_socket.sendto(data_packet, self.server_address)

                block_number += 1
                data = file.read(512)

if __name__ == "__main__":
    # 명령행 인자를 통해 호스트 주소, 포트 번호, 작업(다운로드 또는 업로드), 파일명을 입력받음
    if len(sys.argv) < 4 or (sys.argv[3] == "put" and len(sys.argv) < 5):
        print("Usage: mytftp <host_address> [-p <port_number>] [get|put] <filename>")
        sys.exit(1)

    host_address = sys.argv[1]
    port_number = 69

    if "-p" in sys.argv:
        port_index = sys.argv.index("-p")
        port_number = int(sys.argv[port_index + 1])
        sys.argv.pop(port_index)
        sys.argv.pop(port_index)

    operation = sys.argv[2]
    filename = sys.argv[3]

    # TFTPClient 객체 생성 및 작업에 따라 파일 다운로드 또는 업로드 수행
    tftp_client = TFTPClient(host_address, port_number)

    if operation == "get":
        tftp_client.download_file(filename)
    elif operation == "put":
        tftp_client.upload_file(filename)
    else:
        print("Invalid operation. Use 'get' or 'put'.")
