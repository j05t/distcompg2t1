# distcompg2t2
Distributed Computing Project Group 2 Team 2 Distributed MD5 cracker. 
The system uses one queue per worker for  simplicity's sake.

## Setup
### installation of rabbitmq
sudo apt install rabbitmq-server
### optional: enable management interface on http://localhost:15672
rabbitmq-plugins enable rabbitmq_management
### install Python module for workers
pip3 install pika
### Download and install hashcat
https://hashcat.net

## Usage
### start message queue service
rabbitmqctl start
### start workers
worker_bruteforce.py &
worker_dict.py &
worker_gpu.py &
### start http server on port 1337
node ws_server.js
### use web interface
navigate to http://localhost:1337