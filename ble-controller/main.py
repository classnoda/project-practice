import asyncio
import os
from bleak import BleakClient
from pynput import keyboard

ADDRESS = os.getenv("ADDRESS")
CHARACTERISTIC_UUID = os.getenv("CHARACTERISTIC_UUID")

available_keys = ['w', 'a', 's', 'd', 'e', 'r']


def handler(client, loop):
    def on_press(key):
        try:
            if hasattr(key, 'char'):
                if key.char == 'q':
                    print("Выход...")
                    loop.stop()
                    return False

                if key.char in available_keys:
                    asyncio.run_coroutine_threadsafe(
                        client.write_gatt_char(CHARACTERISTIC_UUID, key.char.encode()),
                        loop
                    )
                else:
                    print(f'{key.char} — не используется')
        except Exception as e:
            print(f'Ошибка: {e}')

    return on_press


async def main():
    print(f"Попытка подключения к {ADDRESS}...")
    async with BleakClient(ADDRESS) as client:
        if client.is_connected:
            print('Подключено! Управляйте (W, A, S, D), выход на Q.')
            loop = asyncio.get_running_loop()
            with keyboard.Listener(on_press=handler(client, loop)) as listener:
                while client.is_connected and listener.running:
                    await asyncio.sleep(0.1)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
