** This is a work in progress **

## Goal

This project emulates a Xemex CSMB which is used by the Shell Recharge 3.0 Advanced wall Charger

## Working

ESPhome acting as a Xemex CSMB by simulating a Modbus RTU Slave/Client/Server that can be polled by a master (e.g. a EV Wallbox like Shell Recharge Advanced 3.0) and delivers IREGs and HREGs which can be controlled arbitratily. Currently I'm including an automation that uses values from my Shelly 3EM. It's based on the work from [NMOptimization](https://community.home-assistant.io/u/NMOptimization). Originally posted on a thread called [My New Motion integration EV Charging from Shell newmotion](https://community.home-assistant.io/t/my-new-motion-integration-ev-charging-from-shell-newmotion/369593/153)

The Xemex CSMB is used to measure the current on up to 3 phases in the home. Based on the actual power consumption, the Shell Recharge 3.0 can decrease or increase the power consumed by the connected car.

## External Documentation

### Documentation on the Xemex CSMB

https://xemex.eu/products/meters-sensors/csmb/  
https://xemex.eu/wp-content/uploads/2021/07/User-manual-CSMB-1.0.pdf  
Page 9 of the user manual contains info on the supported modbus functions.

### Install guides of Shell Advanced Recharge 3.0

https://a.storyblok.com/f/85281/x/e035ddb473/17srqic01_advanced-3-0_quick-installation-guide.pdf  
https://my-instructions.com/shellrecharge/advanced-3.0/?locale=en-GB

### General Modbus Info

https://esphome.io/components/modbus_controller.html  
https://www.modbustools.com/modbus.html

## Next steps

1. Connect a

Connect the ESPHome device to the A and B wires that go to the wallbox and starting feeding it with data.

## Hardware

### The ESP32 Board I used

Link to product page on [Azdelivery.de](https://www.az-delivery.de/en/collections/alle-produkte/products/esp32-developmentboard)

![ESP32 NODEMCU](/pictures/esp32-nodemcu-module-wlan-wifi-development-board-mit-cp2102-nachfolgermodell-zum-esp8266-kompatibel-mit-arduino-872375_400x.webp)

### The RS485 module I used

Link to [amazon.com.be](https://www.amazon.com.be/-/nl/Fasizi-RS485-adapter-seri%C3%ABle-aansluiting/dp/B09Z2GTMJ8/)

![RS485-module](https://raw.githubusercontent.com/thomase1234/esphome-fake-xemex-csmb/thomas-dev/pictures/RS485_Adapter.jpg)
