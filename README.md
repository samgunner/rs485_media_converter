# RS485 to IP converter
This has been specifically designed to pass measurements between an RS485 electricity meter and an AlphaESS Smile5 house battery.
A raspberry pi is required at each end of the link, i.e. one by the battery and one by the meter.

# RS485 on the Raspberry Pi
This required RS485 to UART conversion hardware. I have been using the RS485 hat for the Raspberry Pi. A link to the hardware is here:
https://www.abelectronics.co.uk/p/77/rs485-pi?srsltid=AfmBOooEocKsejZspON-KtAZMtQv2cWWVNQcaGUNDKKkngf_jpABrHri

The instructions for getting the RS495 working on the Raspberry Pi are here:
https://www.abelectronics.co.uk/kb/article/1035/serial-port-setup-in-raspberry-pi-os

# Dependancies
The code is in Python, and requires the installation of:

sudo apt install python-paho-mqtt python-serial

Messages are sent via MQTT, so a working MQTT broker is also required. I am using the Emonpi, which has a broker by default.

# Installation
This must be carried out on both of the Raspberry Pis.
Downlaod the code, and unzip if required.
The code can be run simply as a script. The code must be told here it is (using the --location flag), and you can use the debug flag if you want to see the messages.

python3 converter.py -l meter -d

it doesn't actually matter if you get the locations the right way round, but they do need to be different. This is because requests and responces go on different MQTT topics.

To run as a service, update the service file rs485_converter.service and make sure that the line:

ExecStart=/usr/bin/python3 /home/rs485/code/RS485_media_converter/converter.py -l battery

is updated to point to wherever your converter.py file is, and provide the correct location. Then copy the service file to:

sudo cp rs485_converter.service /etc/systemd/system/

Then enable the service:

sudo systemctl enable rs485_converter.service


