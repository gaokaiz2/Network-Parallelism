sudo chmod 777 /data
cd /data

#install cuda
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-5

sudo apt-get install -y nvidia-driver-555-open
sudo apt-get install -y cuda-drivers-555

#install docker && nvidia-docker && initialize docker
sudo apt update && \
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common && \
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/docker-archive-keyring.gpg > /dev/null && \
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null && \
sudo apt update && \
sudo apt install -y docker-ce

curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get install cuda-toolkit
sudo apt-get install -y nvidia-container-toolkit

sudo systemctl stop docker
sudo mkdir -p /data/docker
echo '{ "data-root": "/data/docker" }' | sudo tee /etc/docker/daemon.json
sudo systemctl start docker


#pull pytorch docker && set up megatron
echo 'ZzhiOGszaW0ydDM4dDYzY3I2bWZudHMzNTI6YjVjN2E1ZDYtMmRlNy00ZTYwLWFlOTYtZDJjMTBmMmY3NTBl' | docker login nvcr.io --username '$oauthtoken' --password-stdin && \
sudo docker pull nvcr.io/nvidia/pytorch:24.05-py3
mkdir /data/workspace

sudo docker run --gpus all -it --rm -v /data/workspace:/data/workspace nvcr.io/nvidia/pytorch:24.05-py3