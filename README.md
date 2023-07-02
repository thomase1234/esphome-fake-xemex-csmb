** This is a work in progress **

## Goal 
This project emulates a Xemex CSMB which is used by the Shell Recharge 3.0 Advanced wall Charger

## Working
ESPhome acting as a Slave/Client/Server that can be polled by a master (e.g. a solar inverter) and delivers IREGs and HREGs which can be controlled arbitratily, I'm planning to use the values from my Shelly EM, however I've included a return value examples that allows you to set the values directly from HomeAssistant for anyone using that.

## Next steps
Connect it to an inverter, enable export control in the inverter menu, and monitor the requests. I've just moved house and my inverter is in a box, so id anyone wants to try this and give me some feedback I would be greatful.



``` yaml
esphome:
  name: sdm230-test04
  friendly_name: sdm230-test04

esp32:
  board: esp32dev
  framework:
    type: arduino

# Enable logging
logger:

# Enable Home Assistant API
api:
  encryption:
    key: "xxxxxx"

ota:
  password: "xxxxxx"

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password

  # Enable fallback hotspot (captive portal) in case wifi connection fails
  ap:
    ssid: "Sdm230-Test04 Fallback Hotspot"
    password: "xxxxxx"

captive_portal:

external_components:
  - source: github://That-Dude/esphome-fake-eastron-SDM230@master
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
        - start_address: 01
          default: 035 # Line to neutral Volts
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.
            
        - start_address: 06
          default: 0 # current Amps
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.
        - start_address: 07
          default: 2 # current Amps
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.

        - start_address: 12
          default: 52 # Active Power Watts
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.   
        - start_address: 13
          default: 30 # Active Power Watts
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.   

        # Request 1 ends here -----------------------------------------------------------------



        - start_address: 18
          default: 52 # Apparent power VoltAmps
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.   
        - start_address: 19
          default: 52 # Apparent power VoltAmps
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.   

        - start_address: 24
          default: 0 # Reactive power VAr
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.
        - start_address: 25
          default: 0003 # Reactive power VAr
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.   

        - start_address: 30
          default: 0 # Power factor
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.
        - start_address: 31
          default: 0 # Power factor
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.   

        - start_address: 36
          default: 0 # Phase angle Degree - this is a guess??? But I don't think it's used anyway
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.
        - start_address: 37
          default: 0 # Phase angle Degree - this is a guess??? But I don't think it's used anyway
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.   

        - start_address: 70
          default: 50 # Frequency Hz
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.   
        - start_address: 71
          default: 0 # Frequency Hz
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.   

        - start_address: 72
          default: 0 # Import active energy kwh
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.   
        - start_address: 73
          default: 0034 # Import active energy kwh
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.   

        - start_address: 74
          default: 0 # Export active energy kwh
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.   
        - start_address: 75
          default: 0 # Export active energy kwh
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else. 

        - start_address: 76
          default: 0 # Import reactive energy kvarh
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.
        - start_address: 77
          default: 034 # Import reactive energy kvarh
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.   

        - start_address: 78
          default: 0 # Export reactive energy kvarh
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.
        - start_address: 79
          default: 0 # Export reactive energy kvarh
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.   

        - start_address: 84
          default: 0 # Total system power demand W
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.
        - start_address: 85
          default: 0 # Total system power demand W
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.   

        - start_address: 86
          default: 200 #  Maximum total system power demand W
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.
        - start_address: 87
          default: 0 # Maximum total system power demand W
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.   

        - start_address: 88
          default: 200 #  Current system positive power demand W
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.
        - start_address: 89
          default: 0 # Current system positive power demand W
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.   

        - start_address: 90
          default: 200 #  Maximum system positive power demand W
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.
        - start_address: 91
          default: 0 # Maximum system positive power demand W
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.   

        - start_address: 92
          default: 0 #  Current system reverse power demand W
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.
        - start_address: 93
          default: 0 # Current system reverse power demand W
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.   

        - start_address: 94
          default: 0 #  Maximum system reverse power demand W
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.
        - start_address: 95
          default: 0 # Maximum system reverse power demand W
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.   

        - start_address: 258
          default: 0 #  Current demand Amps
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.
        - start_address: 259
          default: 0 # Current demand Amps
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.  

        - start_address: 264
          default: 0 #  Maximum Current demand Amps
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.
        - start_address: 265
          default: 0 # Maximum Current demand Amps
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.  

        - start_address: 342
          default: 0 #  Total active energy kwh
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.
        - start_address: 343
          default: 0 #  Total active energy kwh
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.  

        - start_address: 344
          default: 0 #  Total reactive energy kvarh
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.
        - start_address: 345
          default: 0 #  Total reactive energy kvarh
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.  

        - start_address: 384
          default: 0 #  Current resettable total active energy kwh
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.
        - start_address: 385
          default: 0 #  Current resettable total active energy kwh
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.  

        - start_address: 386
          default: 0 #  Current resettable total reactive energy kvarh
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.
        - start_address: 387
          default: 0 #  Current resettable total reactive energy kvarh
          number: 1
          on_read:
            ESP_LOGI("ON_READ", "This is a lambda. address=%d, value=%d", address, value);
            return value; // you can return the stored value or something else.  

            # example return based on the value of tspd number template below
            # return id(tspd).state; // you can return the stored value or something else.


# Creates a number slider in Home Assistant that allows you to set the value of a register
number:
  - platform: template
    name: "Total system power demand W"
    id: tspd
    optimistic: true
    min_value: 0 # this is the default on boot
    max_value: 10000
    step: 100
```

## The module I used
![RS485-module-shield](https://user-images.githubusercontent.com/6509533/230406441-bd38df26-a72c-4a37-88c1-631ec2d2cfe7.jpg)

## Inverter modbus connection
Growatt MIN 3600TL-X

![Screenshot 2023-04-07 at 13 53 21](https://user-images.githubusercontent.com/6509533/230619695-b52cfe74-9f23-4acf-a55b-52fefa3c8346.jpg)
