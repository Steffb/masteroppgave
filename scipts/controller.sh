cd ~/Dropbox/NTNU/Master/pox/masteroppgave
#sudo python pox.py openflow.of_01 --port=6635 forwarding.mycontroller samples.pretty_log info.packet_dump log.level --DEBUG


#sudo python pox.py openflow.of_01 --port=6635 forwarding.clean_up samples.pretty_log info.packet_dump log.level --DEBUG


echo $1

cd ~/Dropbox/NTNU/Master/pox/masteroppgave
# bash check if directory exists
if [ $1 = "controller" ]; then
	sudo python pox.py openflow.of_01 --port=6635 forwarding.mycontroller samples.pretty_log info.packet_dump log.level --DEBUG
	echo "Running controller"
elif [ $1 = "clean" ]; then
	echo "Running cleanup"
	sudo python pox.py openflow.of_01 --port=6635 forwarding.clean_up samples.pretty_log info.packet_dump log.level --DEBUG
else 
	echo "no argument given"
fi 
