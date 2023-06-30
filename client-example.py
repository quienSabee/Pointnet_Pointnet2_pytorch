import socket
import struct
import math

server_ip = "127.0.0.1"
server_port = 42069
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

request_format = "fffff"
# request : float
# h_step_size : float
# v_step_size : float
# h_fov : float
# v_fov : float
# capture_range : float

response_header_format = "i" 
# response_header
# int : point_count

lidarhit_format = "ffffffii" 
# lidarhit
# x, y, z : float, float, float
# nx, ny, nz : float, float, float
# color : int
# classification : int

client_socket.connect((server_ip, server_port))
try:
    h_step_size = float(1)
    v_step_size = float(1)
    h_fov = float(300)
    v_fov = float(100)
    capture_range = float(100)
    request_struct = (h_step_size, v_step_size, h_fov, v_fov, capture_range)
    request_data = struct.pack(request_format, *request_struct)
    client_socket.sendall(request_data)

    response_header_size = struct.calcsize(response_header_format)
    response_header_data = client_socket.recv(response_header_size)
    header_data = struct.unpack(response_header_format, response_header_data)
    point_count = header_data[0]

    lidarhit_size = struct.calcsize(lidarhit_format)
    batch_size = 64
    batch_count = math.ceil(point_count / batch_size)
    count = 0
    for batch_index in range(batch_count):
        response_lidarhit_batch_data = client_socket.recv(batch_size * lidarhit_size)
        lidarhit_array_data = list(struct.iter_unpack(lidarhit_format, response_lidarhit_batch_data))
        for lidar_hit  in lidarhit_array_data:
            position = lidar_hit[0:3]
            normal = lidar_hit[3:6]
            color = lidar_hit[6]
            classification = lidar_hit[7]
            print(f"{position} {normal} {color} {classification}")
            count += 1
    print(f"{count} / {point_count}")
finally:
    client_socket.close()