** This is a work in progress **

## Goal

This project emulates a Xemex CSMB which is used by the Shell Recharge 3.0 Advanced wall Charger

## Working

ESPhome acting as a Xemex CSMB by simulating a Modbus RTU Slave/Client/Server that can be polled by a master (e.g. a EV Wallbox like Shell Recharge Advanced 3.0) and delivers IREGs and HREGs which can be controlled arbitratily, I'm planning to use the values from my Shelly EM, however I've included a return value examples that allows you to set the values directly from HomeAssistant for anyone using that.

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

Connect it to an inverter, enable export control in the inverter menu, and monitor the requests. I've just moved house and my inverter is in a box, so id anyone wants to try this and give me some feedback I would be greatful.

```yaml
esphome:
  name: modbus-server-xemex
  friendly_name: modbus-server-xemex

esp32:
  board: nodemcu-32s
  #https://www.az-delivery.de/en/products/esp32-developmentboard

  framework:
    type: arduino

## start common.yaml

logger:

api:
  encryption:
    key: !secret api_encryption_key

ota:
  password: !secret ota_password

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password
  #fast_connect: on
  domain: !secret domain

  ap:
    ssid: ${device_name} AP
    password: !secret hotspot_pass

captive_portal:

  # Enable Web server
web_server:
  port: 80

text_sensor:
  - platform: wifi_info
    ip_address:
      name: "${device_name} - IP Address"
    ssid:
      name: "${device_name} - Wi-Fi SSID"
    bssid:
      name: "${device_name} - Wi-Fi BSSID"
  - platform: version
    name: "${device_name} - ESPHome Version"
    hide_timestamp: true

# see: https://esphome.io/components/time.html
time:
  - platform: homeassistant
#    id: homeassistant_time

## end common.yaml

external_components:
  - source: github://thomase1234/esphome-fake-xemex-csmb@thomas-dev
    refresh: 60s
    components:
      - modbus_server

uart:
  - id: intmodbus
    tx_pin: 17 # DI WHITE wire
    rx_pin: 16 # RO BLUE  wire
    baud_rate: 9600
    stop_bits: 1
    data_bits: 8
    parity: NONE
    debug:
      direction: BOTH

modbus_server:
  - id: modbuserver
    uart_id: intmodbus
    address: 1 # slave address
    #  - I used this module which reqired pins below http://domoticx.com/wp-content/uploads/2018/01/RS485-module-shield.jpg
    re_pin: GPIO19 # optional
    de_pin: GPIO18 # optional

    # holding_registers: # I don't think these are required for my purposes
    #   - start_address: 79 # starting register range
    #     default: 82 # default value for all those registers
    #     number: 2 # number of registers in the range
    #     on_read: | # called whenever a register in the range is read
    #       // 'address' contains the requested register address
    #       // 'value' contains the stored register value
    #       ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
    #       return value; // you can return the stored value or something else.

    input_registers:
      # I've implimented all of the regs found in this PDF:
      # https://www.eastroneurope.com/images/uploads/products/protocol/SDM630_MODBUS_Protocol.pdf

      # However, most inverters are likely to only request (or only use) certain values.
      # E.g. My Growatt TLX3600 modbus master connected to mobus port B, requests first 14 regs
      # initially (01 04 00 00 00 0E 71 CE)

      - start_address: 00
        default: 240 # Line to neutral Volts
        number: 1
        on_read:
          ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
          return value; // you can return the stored value or something else.
```

## The module I used

![RS485-module-shield](https://user-images.githubusercontent.com/6509533/230406441-bd38df26-a72c-4a37-88c1-631ec2d2cfe7.jpg)

## Inverter modbus connection

Growatt MIN 3600TL-X

![Screenshot 2023-04-07 at 13 53 21](https://user-images.githubusercontent.com/6509533/230619695-b52cfe74-9f23-4acf-a55b-52fefa3c8346.jpg)
