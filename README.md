## Goal

This project tries to set the charge speed of a Shell Recharge 3.0 Advanced wall Chargerby emulating a Xemex CSMB.

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

1. Connect ESP32 dev board to RS485 module.
2. Connect RS485 A and B connectors to the A and B wire that goes to the Shell Recharge 3.0 Wallbox.
3. Build and flash the firmware based on the [sample ESPHome config](/esphome-xemex-fake-modbus-server.yaml).
4. Add new device in HomeAssistant.
5. Now you should be able to set the ctXcurrent numbers. When you set them using HomeAssistant, the values are also reported to your Wallbox.
6. Setup an automation to configure the charge speed. Here you can find a [charge automation](/charge_automation.yaml)

## Interesting info

- My house has a single phase - 40 A connection to the power grid. The house also has a photovoltaic installation that delivers up to 5kW peak. My automation tries to optime power consumption from the sun.
- [In a sister project](https://github.com/thomase1234/esphome-modbus-client-xemex-csmb), I've pulled all data from my Xemex CSMB.
- The real CSMB has 1 CT connected to CT1. Using my custom modbus client, I could see that the register for CT1 contained the actual current. The other to registers ( CT2 and CT3 ) had a non-changing value, which I took over in the ESPHome config.
- Immediately after booting, the Shell Recharge 3.0 Wallbox first requests the Device Code register (0x4002). It expects '20802' as a response. If not, it'll continue retrying.
- The Shell Recharge 3 Wallbox requests the 3 CT registers every 2 seconds.
- This table shows how much Watts the connected car would start consuming after setting the CT3 register to a certain A. F.e. When I set CT3 to 18 ( Amps ), the car started consuming 4550 Watt.

![Amd to Consumption](/pictures/amp_to_consumption.png)

## Unexplicable behaviour

- I couldn't influence the Wallbox by playing around with CT1. This I cannot explain. The real Xemex CSMB only used CT1 as far as my Modbus client showed.
- I could influence the charge speed by playing with the Current in CT3.
  That's strange, as my installation is supposed to use the measurements from CT1.

## Hardware

### The ESP32 Board I used

Link to product page on [Azdelivery.de](https://www.az-delivery.de/en/collections/alle-produkte/products/esp32-developmentboard)

![ESP32 NODEMCU](/pictures/esp32-nodemcu-module-wlan-wifi-development-board-mit-cp2102-nachfolgermodell-zum-esp8266-kompatibel-mit-arduino-872375_400x.webp)

### The RS485 module I used

Link to [amazon.com.be](https://www.amazon.com.be/-/nl/Fasizi-RS485-adapter-seri%C3%ABle-aansluiting/dp/B09Z2GTMJ8/)

![RS485-module](/pictures/RS485_Adapter.jpg)
