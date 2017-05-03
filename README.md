# distcompg2t2
Distributed Computing Project Group 2 Team 2

Setup
=====

# start service
rabbitmqctl start_app

# enable management interface on http://localhost:15672
rabbitmq-plugins enable rabbitmq_management

# install Python module
pip3 install pika


Usage
=====

# start workers
./worker_bruteforce.py &
./worker_dict.py &
./worker_gpu.py &

# create new distributed task
./new_task.py MYHASHVALUEHERE

