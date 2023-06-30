@echo off
docker run --gpus all -it -v .:/notebook/pointnet2 -p 8888:8888 morpheus-pytorch
