import time

from machine import SPI, Pin

from config import Config
from modules.Led import Led
from modules.MRFC522 import MFRC522


class RfId:
    def __init__(self):
        self.led = Led()
        sck = Pin(Config.SCK_PIN, Pin.OUT)
        mosi = Pin(Config.MOSI_PIN, Pin.OUT)
        miso = Pin(Config.MISO_PIN, Pin.OUT)
        self.spi = SPI(2, baudrate=1000000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)

        self.sda = Pin(Config.SDA_PIN, Pin.OUT)
        self.rst = Pin(Config.RST_PIN, Pin.OUT)

        self.rst.value(0)
        time.sleep_ms(20)
        self.rst.value(1)
        time.sleep_ms(20)

        self.reader = MFRC522(self.spi, self.sda)
        self.keys = [
            [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],
            [0x42, 0x52, 0x45, 0x41, 0x4B, 0x4D],
            [0xA0, 0xA1, 0xA2, 0xA3, 0xA4, 0xA5],
            [0xD3, 0xF7, 0xD3, 0xF7, 0xD3, 0xF7],
        ]

    def data_to_string(self, data):
        """Преобразует список байт в читаемую строку."""
        if not data:
            return ""
        # Фильтруем только печатные символы ASCII
        return "".join([chr(x) for x in data if 32 <= x <= 126]).strip()

    def try_read_ntag(self, uid, start_page):
        """Чтение данных из NTAG с обработкой разного поведения библиотек."""
        if self.reader.select_tag(uid) != self.reader.OK:
            return None

        # Вызываем чтение
        result = self.reader.read(start_page)

        # Если библиотека вернула (stat, data)
        if isinstance(result, tuple) or isinstance(result, list) and len(result) == 2:
            stat, data = result
            if stat == self.reader.OK:
                return data
        # Если библиотека вернула сразу список байтов (16 байт для NTAG)
        elif isinstance(result, (list, bytearray)) and len(result) >= 4:
            return result

        return None

    def parse_ndef_text(self, payload):
        """Очищает NDEF заголовок и возвращает чистый текст."""
        try:
            # Ищем байт 0x54 (буква 'T'), после которой идет заголовок языка
            if 0x54 in payload:
                t_index = payload.index(0x54)
                lang_len = payload[t_index + 1]  # Обычно 2 (для 'en')
                text_start = t_index + 2 + lang_len
                return "".join([chr(x) for x in payload[text_start:] if 32 <= x <= 126])
        except:
            pass
        return self.data_to_string(payload)  # Fallback

    def parse_ndef_text(self, payload):
        """Извлекает только текст из NDEF записи, отсекая заголовки и маркеры конца."""
        try:
            if 0x54 in payload:  # Ищем маркер 'T' (Text)
                t_idx = payload.index(0x54)
                # payload[t_idx + 1] — это длина кода языка (например, 2 для 'en')
                lang_len = payload[t_idx + 1]
                start = t_idx + 2 + lang_len

                # Ищем маркер конца NDEF (0xFE) или берем до конца
                raw_extracted = payload[start:]
                if 0xFE in raw_extracted:
                    raw_extracted = raw_extracted[:raw_extracted.index(0xFE)]

                # Декодируем только печатные ASCII символы
                return "".join([chr(x) for x in raw_extracted if 32 <= x <= 126]).strip()
        except:
            pass
        return ""

    def loop(self):
        print('RFID Reader Ready...')
        while True:
            try:
                (stat, tag_type) = self.reader.request(self.reader.REQIDL)
                if stat == self.reader.OK:
                    res = self.reader.anticoll()
                    uid = res[1] if (isinstance(res, tuple) and len(res) == 2) else res

                    if uid:
                        if self.reader.select_tag(uid) == self.reader.OK:
                            full_raw = []
                            for page in [4, 8]:
                                result = self.reader.read(page)
                                data = result[1] if (isinstance(result, tuple) and len(result) == 2) else result
                                if data:
                                    full_raw.extend(list(data))

                            if full_raw:
                                text = self.parse_ndef_text(full_raw)
                                if text:
                                    uid_hex = "".join(["%02x" % i for i in uid])
                                    print(f"UID: {uid_hex} | Text: {text}")
                                    self.led.handler(text)

                            self.reader.antenna_on(False)
                            time.sleep_ms(10)
                            self.reader.antenna_on(True)
                time.sleep_ms(500)
                self.led.handler()
            except Exception:
                print("RFID Reader Error")
                for _ in range(3):
                    self.led.set((10, 0, 0))
                    time.sleep_ms(300)
                    self.led.set((0, 0, 0))
                    time.sleep_ms(300)
