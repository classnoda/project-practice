import struct
from bluetooth import BLE, UUID, FLAG_WRITE, FLAG_NOTIFY
from bluetooth import FLAG_READ


class BLE_Controller():
    def __init__(self, name, handler):
        self.handler = handler

        self.ble = BLE()
        self.ble.active(True)

        self.ble.irq(self.ble_irq_handler)
        self.__init_tx_rx()

        self.ble.gap_advertise(100_000, self.advertising_payload(name))

    def __init_tx_rx(self):
        HR_UUID = UUID(0x180D)
        HR_CHAR = (UUID(0x2A37), FLAG_READ | FLAG_NOTIFY,)
        HR_SERVICE = (HR_UUID, (HR_CHAR,),)
        UART_UUID = UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')
        UART_TX = (UUID('6E400003-B5A3-F393-E0A9-E50E24DCCA9E'), FLAG_READ | FLAG_NOTIFY,)
        UART_RX = (UUID('6E400002-B5A3-F393-E0A9-E50E24DCCA9E'), FLAG_WRITE,)
        UART_SERVICE = (UART_UUID, (UART_TX, UART_RX,),)
        SERVICES = (HR_SERVICE, UART_SERVICE,)
        ((hr,), (self.tx, self.rx,),) = self.ble.gatts_register_services(SERVICES)

    def advertising_payload(self, name: str):
        payload = bytearray()
        payload += struct.pack("BBB", 2, 0x01, 0x06)
        payload += struct.pack("BB", len(name) + 1, 0x09) + name.encode()

        return payload

    def ble_irq_handler(self, event, data):
        if event == 3:
            conn_handle, value_handle = data
            if value_handle == self.rx:
                msg = self.ble.gatts_read(self.rx)
                self.handler(msg)