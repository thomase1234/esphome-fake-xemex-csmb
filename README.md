## Goal

This project allows you to set the charge speed of a Shell Recharge Advanced 3.0 charging point by emulating a Xemex CSMB.

## How is this working ?

ESPhome device acting as a Xemex CSMB by simulating a Modbus RTU Slave/Client/Server that can be polled by a master (e.g. a EV Wallbox like Shell Recharge Advanced 3.0) and delivers IREGs and HREGs which can be controlled arbitrarily. Currently I'm including a Home Assistant automation that uses values from my Shelly 3EM. It's based on the work from [NMOptimization](https://community.home-assistant.io/u/NMOptimization). Originally posted on a thread called [My New Motion integration EV Charging from Shell newmotion](https://community.home-assistant.io/t/my-new-motion-integration-ev-charging-from-shell-newmotion/369593/153)

The Xemex CSMB is used to measure the current on up to 3 phases. Based on the actual current measurements, the Shell Recharge 3.0 can decrease or increase the power that can be consumed by the connected car.

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

## How to set up the hardware ?

1. Connect ESP32 dev board to RS485 module.
2. Connect RS485 A and B connectors to the A and B wire that goes to the Shell Recharge 3.0 Wallbox.
3. Build and flash the firmware based on the [sample ESPHome config](/esphome-xemex-fake-modbus-server.yaml).
4. Add new device in HomeAssistant.
5. Now you should be able to set the ctXcurrent numbers. When you set them using HomeAssistant, the values are also reported to your Wallbox.
6. Setup an automation to configure the charge speed. Here you can find a [charge automation](/charge_automation.yaml)
7. Set the input_number main_maximal_current to the correct value

## Interesting info

- My house has a single phase - 40 A connection to the power grid. The house also has a photovoltaic installation that delivers up to 5kW peak. My automation tries to optime power consumption from the sun.
- [In a sister project](https://github.com/thomase1234/esphome-modbus-client-xemex-csmb), I've pulled all data from my Xemex CSMB.
- The real CSMB has 1 CT connected to CT1. Using my custom modbus client, I could see that the register for CT1 contained the actual current. The other to registers ( CT2 and CT3 ) had a non-changing value, which I took over in the ESPHome config.
- Immediately after booting, the Shell Recharge 3.0 Wallbox first requests the Device Code register (0x4002). It expects '20802' as a response. If not, it'll continue retrying.
- The Shell Recharge 3 Wallbox requests the 3 CT registers every 2 seconds.
- You have to know what the max Current ( in Amps ) setting is on your Wallbox. In my case, this was set to 37.8 Amps. As soon as the fake CSMB starts reporting values higher than 37.8 Amps, my charging would decrease. Set the input_number main_maximal_current to the correct value.

## How to use the Home Assistant automation ?

Some info on the sensors that I used in the [Automation](/charge_automation.yaml).

- shell3em_main_current is the current on my cable between grid and house. This number is always positive, even if my house ( thanks to the pv - solar panels ) is producing more electricity than it consumes. If it reads 5 Amp, it can be that my house is consuming 5 Amp from the grid, or it can be that my house is delivering 5 Amp to the grid.

- shell3em_main_power_factor is the power factor which ranges between -1 and 1. If the number is negative, that means that my house is producing more energy than it consumes which means that the excess energy is delivered to the grid. If the number is positive, the house is consuming from the grid. Usually the value is either very close to 1 when consuming, or very close to -1 when delivering to the grid.

Multiplying the 2 previous parameters give me a single number with the total of Amps consumed. Negative numbers for delivering.

- shelly3em_laadpaal_current is the current on the "laadpaal". "Laadpaal" is Dutch for Wall Charger. Since I know that the Wall Charger will always consume energy, I didn't multiply the number with its corresponding power_factor.

### The different Charge Modes

In one of my dashboards I created a dropdown menu which allows me to set the charge mode that is used by the [charge automation](/charge_automation.yaml).

![Charge Mode Selector](/pictures/HomeAssistant_ChargeMode.png)

## Hardware

### Wiring

Note that this show the wiring that I created. Other configurations are possible.

Power: I removed the micro-usb plug from an old USB cable and looked for the Ground (GND) and +5V wires. Using a bread board, I made the following connections.

- connect the GND wire from the USB cable to both a GND Pin on the ESP32 and the GND Pin on the RS485.
- connect the -5V wire from the USB cable to both the 5V Pin on the ESP32 and the VCC Pin on the RS485.

Data

- connect a wire between the ESP32 G18 and the RS485 TXD Pin
- connect a wire between the ESP32 G19 and the RS485 RXD Pin

### The ESP32 Board I used

Link to product page on [Azdelivery.de](https://www.az-delivery.de/en/collections/alle-produkte/products/esp32-developmentboard)

![ESP32 NODEMCU](/pictures/esp32-nodemcu-module-wlan-wifi-development-board-mit-cp2102-nachfolgermodell-zum-esp8266-kompatibel-mit-arduino-872375_400x.webp)
![Pinout Diagram](/pictures/ESP_-_32_NodeMCU_Developmentboard_Pinout_Diagram.jpg)

### The RS485 module I used

Link to [amazon.com.be](https://www.amazon.com.be/-/nl/Fasizi-RS485-adapter-seri%C3%ABle-aansluiting/dp/B09Z2GTMJ8/)

![RS485-module](/pictures/RS485_Adapter.jpg)
