FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-devel
RUN apt-get update && apt-get install -y git
RUN pip install jupyter
# RUN git clone https://github.com/yanx27/Pointnet_Pointnet2_pytorch.git
WORKDIR /notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root"]
