#!/bin/bash

# create function for a nice abort
terminate_progs() {
	kill -SINGINT $pid1
	kill -SINGINT $pid2
	echo "Programs aborted"
	exit 0
}

# activate virtual environment
echo "Activating env"
source ~/env/bin/activate

# run led matrix script
echo "Running matrix script"
sudo python3 ~/DART/rpi-rgb-led-matrix/bindings/python/samples/custom_2.py >> matrix_output.txt &
pid1=$!

# wait for led matrix to initalize
echo "Waiting for LED matrix to start"
sleep 3

# run the LED strand script
echo "Running LED Strand script"
sudo --preserve-env=PATH,VIRTUAL_ENV ~/DART/rpi_ws281x/examples/python3 strandtest.py >> strand_output.txt &
pid2=$!

trap terminate_progs SIGINT

while true; do
	read -p "Enter 'q' to quit: " input
	if [[ $input = "q" ]]; then
		terminate_progs
	fi
done


