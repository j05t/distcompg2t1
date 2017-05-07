# distcompg2t2
Distributed Computing Project Group 2 Team 2
Distributed MD5 cracker. The system uses one queue per worker for  simplicity's sake.

## Setup
### installation of rabbitmq
sudo apt install rabbitmq-server
### optional: enable management interface on http://localhost:15672
rabbitmq-plugins enable rabbitmq_management
### install Python module for workers
pip3 install pika


### Setup OpenCL
sudo apt-get install ocl-icd-libopencl1 opencl-headers clinfo

### Download and install hashcat under /usr/local/share/hashcat
https://hashcat.net


## Usage
### start message queue service
rabbitmqctl start

### start workers
workers/worker_bruteforce.py &
workers/worker_dict.py &
workers/worker_gpu.py &

### start http server on port 1337
node webinterface/ws_server.js

### use web interface
navigate to http://localhost:1337