# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# MCP9808
# This code is designed to work with the MCP9808_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Temperature?sku=MCP9808_I2CS#tabs-0-product_tabset-2

import smbus
import time


class MCP9808:
    def __init__(self) -> None:

        # Get I2C bus
        self.bus = smbus.SMBus(1)

        # MCP9808 address, 0x18(24)
        # Select configuration register, 0x01(1)
        # 		0x0000(00)	Continuous conversion mode, Power-up default
        config: list[int] = [0x00, 0x00]
        self.bus.write_i2c_block_data(0x18, 0x01, config)
        # MCP9808 address, 0x18(24)
        # Select resolution rgister, 0x08(8)
        # 		0x03(03)	Resolution = +0.0625 / C
        self.bus.write_byte_data(0x18, 0x08, 0x03)

        time.sleep(0.5)

    def read_temp(self) -> float:
        # MCP9808 address, 0x18(24)
        # Read data back from 0x05(5), 2 bytes
        # Temp MSB, TEMP LSB
        data = self.bus.read_i2c_block_data(0x18, 0x05, 2)

        # Convert the data to 13-bits
        ctemp: float = ((data[0] & 0x1F) * 256) + data[1]
        if ctemp > 4095:
            ctemp -= 8192
        ctemp = ctemp * 0.0625
        return ctemp


if __name__ == "__main__":
    while True:
        print("Temperature in Celsius is : %.2f C" % MCP9808.read_temp)
        time.sleep(1)
