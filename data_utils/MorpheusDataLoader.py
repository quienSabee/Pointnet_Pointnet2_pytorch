# *_*coding:utf-8 *_*
import socket
import struct
import math
import sys
import warnings
import numpy as np
from torch.utils.data import Dataset
warnings.filterwarnings('ignore')

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

class MorpheusDataset(Dataset):
    def __init__(self, server_ip = "127.0.0.1", server_port = 42069, point_batch_size = 64, h_step_size = float(1), v_step_size = float(1), h_fov = float(300), v_fov = float(100), capture_range = float(100)):
        super().__init__()
        self.point_batch_size = point_batch_size
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((server_ip, server_port))
        request_struct = (h_step_size, v_step_size, h_fov, v_fov, capture_range)
        self.request_data = struct.pack(request_format, *request_struct)
    
    def __getitem__(self, index):
        self.send_request()
        x = self.get_response()
        return x

    def __len__(self):
        return sys.maxint
    
    def dispose(self):
        self.client_socket.close()
        
    def send_request(self):
        self.client_socket.sendall(self.request_data)
        
    def get_response(self):
        response_header_size = struct.calcsize(response_header_format)
        response_header_data = self.client_socket.recv(response_header_size)
        header_data = struct.unpack(response_header_format, response_header_data)
        point_count = header_data[0]
        lidarhit_size = struct.calcsize(lidarhit_format)
        batch_count = math.ceil(point_count / self.point_batch_size)
        for batch_index in range(batch_count):
            response_lidarhit_batch_data = self.client_socket.recv(self.point_batch_size * lidarhit_size)
            lidarhit_array_data = list(struct.iter_unpack(lidarhit_format, response_lidarhit_batch_data))
            for lidar_hit  in lidarhit_array_data:
                position = lidar_hit[0:3]
                normal = lidar_hit[3:6]
                color = lidar_hit[6]
                classification = lidar_hit[7]
                
if __name__ == '__main__':
    point_data = MorpheusDataset()
    while (True):
        x = point_data.__getitem__(1)
    