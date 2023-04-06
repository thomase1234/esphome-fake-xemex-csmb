esphome:
  name: sdm-test03
  friendly_name: sdm-test03

esp32:
  board: esp32dev
  framework:
    type: arduino

# Enable logging
logger:

# Enable Home Assistant API
api:
  encryption:
    key: "xxx"

ota:
  password: "xxx"

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password

  # Enable fallback hotspot (captive portal) in case wifi connection fails
  ap:
    ssid: "Sdm-Test03 Fallback Hotspot"
    password: "xxx"

captive_portal:

external_components:
  - source: github://aj-nagrom/esphome-modbus-server@master
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
    holding_registers:
      - start_address: 79 # starting register range
        default: 82 # default value for all those registers
        number: 10 # number of registers in the range
        on_read: | # called whenever a register in the range is read
          // 'address' contains the requested register address
          // 'value' contains the stored register value 
          ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
          return value; // you can return the stored value or something else.

      - start_address: 100 # starting register range
        default: 99 # default value for all those registers
        number: 10 # number of registers in the range
        on_read: | # called whenever a register in the range is read
          // 'address' contains the requested register address
          // 'value' contains the stored register value 
          ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
          return id(tspd).state; // you can return the stored value or something else.


# Creates a number slider in Home Assistant that allows you to set the value of a register
number:
  - platform: template
    name: "Total system power demand W"
    id: tspd
    optimistic: true
    min_value: 0 # this is the default on boot
    max_value: 10000
    step: 100
