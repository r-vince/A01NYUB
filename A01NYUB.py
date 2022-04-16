from machine import Pin
import time


uart = UART(1, baudrate=9600, pins=('P20','P21'))               # Set UART pins.    A01NYUB TX wire to pin 21
trigger = Pin(Pin.exp_board.G16, mode=Pin.OUT)                  #PIN 16 on expansion board 3.1 to RX wire of A01NYUB ultrasonic sensor


def Get_A01NYUB_dist():
    done = False
    distance = 0
    header_val = b'\xff'
    dummy = uart.readline()                                 # Wipe all data in UART Receive
    while True:
        trigger(0)                                          #Not sure but this seems to male the data more stable
        time.sleep_us(2)  #2usec
        trigger(1)
        time.sleep_us(10)  #10usec
        ByteHeader = uart.read(1)                               # Read 1 byte
        if ByteHeader == header_val:                            # is it a header byte = b'\xff'
            ByteHigh = uart.read(1)                             # read high byte
            ByteLow = uart.read(1)                              # read low byte
            Checksum = uart.read(1)                             # read Checksum byte
            ByteHighIntVal = int.from_bytes(ByteHigh,"little")  # convert high byte to integer
            ByteLowIntVal = int.from_bytes(ByteLow,"little")    # convert low byte to integer
            Dist = (ByteHighIntVal * 256) + ByteLowIntVal   # Calculate distance from returned UART data see https://wiki.dfrobot.com/A01NYUB%20Waterproof%20Ultrasonic%20Sensor%20SKU:%20SEN0313
            return Dist

distance = Get_A01NYUB_dist()
print("Dist - " + str(distance) + " - mm")
