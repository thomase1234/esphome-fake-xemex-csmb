import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.cpp_helpers import gpio_pin_expression
from esphome.components import uart
from esphome.const import CONF_ADDRESS, CONF_ID
from esphome import pins

CONF_START_ADDRESS = "start_address"
CONF_DEFAULT = "default"
CONF_NUMBER = "number"
CONF_RE_PIN = "re_pin"
CONF_DE_PIN = "de_pin"
CONF_ON_READ = "on_read"
CONF_ON_WRITE = "on_write"

modbus_server_ns = cg.esphome_ns.namespace("modbus_server")
ModbusDeviceComponent = modbus_server_ns.class_("ModbusServer", cg.Component)

DEPENDENCIES = ["uart"]

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(ModbusDeviceComponent),
            cv.Required(CONF_ADDRESS): cv.positive_int,
            cv.Optional(CONF_RE_PIN): pins.gpio_output_pin_schema,
            cv.Optional(CONF_DE_PIN): pins.gpio_output_pin_schema,
            cv.Optional("holding_registers"): cv.ensure_list(
                cv.Schema(
                    {
                        cv.Required(CONF_START_ADDRESS): cv.positive_int,
                        cv.Optional(CONF_DEFAULT, 0): cv.positive_int,
                        cv.Optional(CONF_NUMBER, 1): cv.positive_int,
                        cv.Optional(CONF_ON_READ): cv.returning_lambda,
                        cv.Optional(CONF_ON_WRITE): cv.returning_lambda,
                    }
                )
            ),
        }
    )
    .extend(uart.UART_DEVICE_SCHEMA)
    .extend(cv.COMPONENT_SCHEMA)
)

MULTI_CONF = True
CODEOWNERS = ["@jpeletier"]


async def to_code(config):

    cg.add_library("emelianov/modbus-esp8266", "4.1.0")
    id = config[CONF_ID]
    uart = await cg.get_variable(config["uart_id"])
    server = cg.new_Pvariable(id)
    cg.add(server.set_uart_parent(uart))
    cg.add(server.set_address(config[CONF_ADDRESS]))

    if CONF_RE_PIN in config:
        pin = await gpio_pin_expression(config[CONF_RE_PIN])
        cg.add(server.set_re_pin(pin))
    if CONF_DE_PIN in config:
        pin = await gpio_pin_expression(config[CONF_DE_PIN])
        cg.add(server.set_de_pin(pin))

    if "holding_registers" in config:
        for reg in config["holding_registers"]:
            cg.add(
                server.add_holding_register(
                    reg[CONF_START_ADDRESS], reg[CONF_DEFAULT], reg[CONF_NUMBER]
                )
            )
            if CONF_ON_READ in reg:
                template_ = await cg.process_lambda(
                    reg[CONF_ON_READ],
                    [
                        (cg.uint16, "address"),
                        (cg.uint16, "value"),
                    ],
                    return_type=cg.uint16,
                )
                cg.add(
                    server.on_read_holding_register(
                        reg[CONF_START_ADDRESS], template_, reg[CONF_NUMBER]
                    )
                )
            if CONF_ON_WRITE in reg:
                template_ = await cg.process_lambda(
                    reg[CONF_ON_WRITE],
                    [
                        (cg.uint16, "address"),
                        (cg.uint16, "value"),
                    ],
                    return_type=cg.uint16,
                )
                cg.add(
                    server.on_write_holding_register(
                        reg[CONF_START_ADDRESS], template_, reg[CONF_NUMBER]
                    )
                )

    await cg.register_component(server, config)

    return
